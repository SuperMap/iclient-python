from http.server import HTTPServer,BaseHTTPRequestHandler,HTTPStatus
from typing import List,Callable
from urllib import parse
from .WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.ElementTree as ET
import logging
import time


logger = logging.Logger(__name__)

_response_msg_format = '''<xml>
<ToUserName><![CDATA[{ToUserName}]]></ToUserName>
<FromUserName><![CDATA[{sCorpID}]]></FromUserName>
<CreateTime>{CreateTime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
<MsgId>1234567890123456</MsgId><AgentID>1</AgentID></xml>'''


def _query_values(path:str, param_names:List[str]):
    kvps =  dict(parse.parse_qsl(parse.urlsplit(path).query))
    return tuple([kvps[name] for name in param_names])

from abc import abstractmethod

class WXHookReceiver(BaseHTTPRequestHandler):

    @abstractmethod
    def get_wxcrypt(self) -> WXBizMsgCrypt:
        pass

    @abstractmethod
    def get_sCorpID(self) -> str:
        pass

    @abstractmethod
    def get_msg_fun(self) -> Callable[[str, str], str]:
        pass

    def call_msg_fun(self, *args, **kwargs):
        try:
            return self.get_msg_fun()(*args, **kwargs)
        except:
            logger.exception('unknown error.')
            return 'Error'

    def send_wx_msg(self,msg:str, to_user_name, sReqNonce):
        sRespData = _response_msg_format.format(content = msg, ToUserName = to_user_name, sCorpID = self.get_sCorpID(), CreateTime=str(int(time.time())))
        ret, msg = self.get_wxcrypt().EncryptMsg(sRespData, sReqNonce)
        if ret != 0:
            logger.warning('EncryptMsg failed:' + str(ret))
            self.finish()
            return
        self.send(msg)

    def send(self, msg: str, status = HTTPStatus.OK):
        byte_content = bytes(msg, encoding='utf-8')
        self.send_response(status)
        self.send_header('Content-Length', str(len(byte_content)))
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(byte_content)

    def do_GET(self):
        sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr = _query_values(self.path, ['msg_signature', 'timestamp', 'nonce', 'echostr'])
        ret, sEchoStr = self.get_wxcrypt().VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        if ret == 0:
            self.send(str(sEchoStr, 'utf8'))
        else:
            logger.warning('VerifyURL failed:' + str(ret))
            self.finish()


    def do_POST(self):
        sReqMsgSig, sReqTimeStamp, sReqNonce = _query_values(self.path, ['msg_signature', 'timestamp', 'nonce'])
        sReqData = self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf-8')
        ret, sMsg = self.get_wxcrypt().DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        if ret != 0:
            logger.warning('DecryptMsg failed:' + str(ret))
            self.finish()
            return
        sMsg = str(sMsg, 'utf-8')
        xml_tree = ET.fromstring(sMsg)
        content = xml_tree.find("Content").text # type:str
        from_user_name = xml_tree.find('FromUserName').text
        self.send_wx_msg(self.call_msg_fun(content, from_user_name), from_user_name, sReqNonce)


def start_server(msg_fun: Callable[[str, str], str], sToken:str, sEncodingAESKey:str, sCorpID:str, port:int , bind_ip: str = '0.0.0.0', server_kls = HTTPServer):
    wxcrypt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    class Handler(WXHookReceiver):

        def get_msg_fun(self):
            return msg_fun

        def get_sCorpID(self):
            return sCorpID

        def get_wxcrypt(self):
            return wxcrypt

    Handler.protocol_version = "HTTP/1.1"
    with server_kls((bind_ip, int(port)), Handler) as httpd:
        httpd.serve_forever()