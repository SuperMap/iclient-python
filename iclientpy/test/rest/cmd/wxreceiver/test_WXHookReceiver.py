from unittest import TestCase
from unittest.mock import MagicMock
from iclientpy.rest.cmd.wxreceiver.server import WXHookReceiver


class WXHookReceiverTest(TestCase):

    def setUp(self):
        self._msg_fun = MagicMock()
        self._crypt = MagicMock()

        class Receiver(WXHookReceiver):

            def __init__(self):
                pass

            def get_wxcrypt(self_handler):
                return self._crypt

            def get_sCorpID(self):
                return 'corpid'

            def get_msg_fun(self_handler):
                return self._msg_fun
        self._receiver = Receiver()
        self._receiver.send_header = MagicMock()
        self._receiver.send_response = MagicMock()
        self._receiver.wfile = MagicMock()
        self._receiver.wfile.write = MagicMock()
        self._receiver.rfile = MagicMock()
        self._receiver.rfile.read = MagicMock()
        self._receiver.end_headers = MagicMock()

    def test_get_success(self):
        self._receiver.path = '/index?msg_signature=4662d1b7a6decfefad3c8e2e0c330e6fb2ec1e6e&timestamp=1530755808&nonce=1530409251&echostr=abc'
        self._crypt.VerifyURL = MagicMock(return_value=(0,'abc'.encode('utf8')))
        self._receiver.do_GET()
        write = self._receiver.wfile.write #type:MagicMock
        write.assert_called_with('abc'.encode('utf8'))

    def test_get_failed(self):
        self._receiver.path = '/index?msg_signature=4662d1b7a6decfefad3c8e2e0c330e6fb2ec1e6e&timestamp=1530755808&nonce=1530409251&echostr=abc'
        self._crypt.VerifyURL = MagicMock(return_value=(-1,None))
        self._receiver.finish = MagicMock()
        self._receiver.do_GET()
        self._receiver.finish.assert_called()

    def test_get_failed(self):
        self._receiver.path = '/index?msg_signature=4662d1b7a6decfefad3c8e2e0c330e6fb2ec1e6e&timestamp=1530755808&nonce=1530409251&echostr=abc'
        self._crypt.VerifyURL = MagicMock(return_value=(1,None))
        self._receiver.do_GET()
        write = self._receiver.wfile.write #type:MagicMock
        write.assert_not_called()

    def test_post_success(self):
        request_body = '<xml><ToUserName><![CDATA[ww211005fad1eca8ba]]></ToUserName><Encrypt><![CDATA[zdNXPCW2tJHGt2NnEk4hD3mIuWXW+1bgR/QnHg2wFtTo2LP+2ALwKyQX+bKQ2a9yoOcDbX/p6s7PT/8RlFngiLhX3biXcEQY1pbSQspmkpCY/0ZjqNpwVoGTlIz7+oEtGf7SMoWAom2b2z3LUW6T8L6OmN24v5HFHETpHYZhVnYUZa1AkGCvI7GwI1wuO0WVNSAB5UNmNdwI42aO/asr1dLNxMDojI3qE7RSRHtbUjPinvRRcykjdJ8AtAryDIPjutOnPTk9zxqmnbxJhfHmsf3SwYu9QBD6IOagKFLF228HClTdiZpWw07kLHnt+an8rOTMTeEPcV40YOMNtq8K11UAYartL635se1Ox1swq/S+hVjNklcbC8aSyCgp9leeX28b+tuN5pAi4HGxjV4kOxIBO7AOgS517+KwrrvY+Fo=]]></Encrypt><AgentID><![CDATA[1000002]]></AgentID></xml>'
        self._receiver.headers = {'Content-Length': len(request_body)}
        read = self._receiver.rfile.read #type: MagicMock
        read.return_value = request_body.encode('utf8')
        self._receiver.path = '/index?msg_signature=4662d1b7a6decfefad3c8e2e0c330e6fb2ec1e6e&timestamp=1530755808&nonce=1530409251&echostr=abc'
        self._crypt.DecryptMsg = MagicMock(return_value=(0,'<xml><ToUserName><![CDATA[ww211005fad1eca8ba]]></ToUserName><FromUserName><![CDATA[GuYongQuan]]></FromUserName><CreateTime>1530771910</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[list]]></Content><MsgId>1958266229</MsgId><AgentID>1000002</AgentID></xml>'.encode('utf8')))
        self._crypt.EncryptMsg = MagicMock(return_value=(0, 'EncryptMsg_send_result'))
        self._msg_fun.return_value = 'send_result'
        self._receiver.do_POST()
        write = self._receiver.wfile.write #type:MagicMock
        write.assert_called_with('EncryptMsg_send_result'.encode('utf8'))
        reply_msg = self._crypt.EncryptMsg.call_args[0][0]
        self.assertIn('GuYongQuan', reply_msg)

    def test_post_exception(self):
        request_body = '<xml><ToUserName><![CDATA[ww211005fad1eca8ba]]></ToUserName><Encrypt><![CDATA[zdNXPCW2tJHGt2NnEk4hD3mIuWXW+1bgR/QnHg2wFtTo2LP+2ALwKyQX+bKQ2a9yoOcDbX/p6s7PT/8RlFngiLhX3biXcEQY1pbSQspmkpCY/0ZjqNpwVoGTlIz7+oEtGf7SMoWAom2b2z3LUW6T8L6OmN24v5HFHETpHYZhVnYUZa1AkGCvI7GwI1wuO0WVNSAB5UNmNdwI42aO/asr1dLNxMDojI3qE7RSRHtbUjPinvRRcykjdJ8AtAryDIPjutOnPTk9zxqmnbxJhfHmsf3SwYu9QBD6IOagKFLF228HClTdiZpWw07kLHnt+an8rOTMTeEPcV40YOMNtq8K11UAYartL635se1Ox1swq/S+hVjNklcbC8aSyCgp9leeX28b+tuN5pAi4HGxjV4kOxIBO7AOgS517+KwrrvY+Fo=]]></Encrypt><AgentID><![CDATA[1000002]]></AgentID></xml>'
        self._receiver.headers = {'Content-Length': len(request_body)}
        read = self._receiver.rfile.read #type: MagicMock
        read.return_value = request_body.encode('utf8')
        self._receiver.path = '/index?msg_signature=4662d1b7a6decfefad3c8e2e0c330e6fb2ec1e6e&timestamp=1530755808&nonce=1530409251&echostr=abc'
        self._crypt.DecryptMsg = MagicMock(return_value=(0,'<xml><ToUserName><![CDATA[ww211005fad1eca8ba]]></ToUserName><FromUserName><![CDATA[GuYongQuan]]></FromUserName><CreateTime>1530771910</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[list]]></Content><MsgId>1958266229</MsgId><AgentID>1000002</AgentID></xml>'.encode('utf8')))
        self._crypt.EncryptMsg = MagicMock(return_value=(0, 'EncryptMsg_send_result'))
        self._msg_fun.side_effect = KeyError('foo')
        self._receiver.do_POST()
        write = self._receiver.wfile.write #type:MagicMock
        reply_msg = self._crypt.EncryptMsg.call_args[0][0]
        self.assertIn('Error', reply_msg)

    def test_post_DecryptMsg_failed(self):
        request_body = '<xml><ToUserName><![CDATA[ww211005fad1eca8ba]]></ToUserName><Encrypt><![CDATA[zdNXPCW2tJHGt2NnEk4hD3mIuWXW+1bgR/QnHg2wFtTo2LP+2ALwKyQX+bKQ2a9yoOcDbX/p6s7PT/8RlFngiLhX3biXcEQY1pbSQspmkpCY/0ZjqNpwVoGTlIz7+oEtGf7SMoWAom2b2z3LUW6T8L6OmN24v5HFHETpHYZhVnYUZa1AkGCvI7GwI1wuO0WVNSAB5UNmNdwI42aO/asr1dLNxMDojI3qE7RSRHtbUjPinvRRcykjdJ8AtAryDIPjutOnPTk9zxqmnbxJhfHmsf3SwYu9QBD6IOagKFLF228HClTdiZpWw07kLHnt+an8rOTMTeEPcV40YOMNtq8K11UAYartL635se1Ox1swq/S+hVjNklcbC8aSyCgp9leeX28b+tuN5pAi4HGxjV4kOxIBO7AOgS517+KwrrvY+Fo=]]></Encrypt><AgentID><![CDATA[1000002]]></AgentID></xml>'
        self._receiver.headers = {'Content-Length': len(request_body)}
        read = self._receiver.rfile.read #type: MagicMock
        read.return_value = request_body.encode('utf8')
        self._receiver.path = '/index?msg_signature=4662d1b7a6decfefad3c8e2e0c330e6fb2ec1e6e&timestamp=1530755808&nonce=1530409251&echostr=abc'
        self._crypt.DecryptMsg = MagicMock(return_value=(1, None))
        self._receiver.finish = MagicMock()
        self._receiver.do_POST()
        self._receiver.finish.assert_called()

    def test_post_EncryptMsg_failed(self):
        request_body = '<xml><ToUserName><![CDATA[ww211005fad1eca8ba]]></ToUserName><Encrypt><![CDATA[zdNXPCW2tJHGt2NnEk4hD3mIuWXW+1bgR/QnHg2wFtTo2LP+2ALwKyQX+bKQ2a9yoOcDbX/p6s7PT/8RlFngiLhX3biXcEQY1pbSQspmkpCY/0ZjqNpwVoGTlIz7+oEtGf7SMoWAom2b2z3LUW6T8L6OmN24v5HFHETpHYZhVnYUZa1AkGCvI7GwI1wuO0WVNSAB5UNmNdwI42aO/asr1dLNxMDojI3qE7RSRHtbUjPinvRRcykjdJ8AtAryDIPjutOnPTk9zxqmnbxJhfHmsf3SwYu9QBD6IOagKFLF228HClTdiZpWw07kLHnt+an8rOTMTeEPcV40YOMNtq8K11UAYartL635se1Ox1swq/S+hVjNklcbC8aSyCgp9leeX28b+tuN5pAi4HGxjV4kOxIBO7AOgS517+KwrrvY+Fo=]]></Encrypt><AgentID><![CDATA[1000002]]></AgentID></xml>'
        self._receiver.headers = {'Content-Length': len(request_body)}
        read = self._receiver.rfile.read #type: MagicMock
        read.return_value = request_body.encode('utf8')
        self._receiver.path = '/index?msg_signature=4662d1b7a6decfefad3c8e2e0c330e6fb2ec1e6e&timestamp=1530755808&nonce=1530409251&echostr=abc'
        self._crypt.DecryptMsg = MagicMock(return_value=(0, '<xml><ToUserName><![CDATA[ww211005fad1eca8ba]]></ToUserName><FromUserName><![CDATA[GuYongQuan]]></FromUserName><CreateTime>1530771910</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[list]]></Content><MsgId>1958266229</MsgId><AgentID>1000002</AgentID></xml>'.encode()))
        self._crypt.EncryptMsg = MagicMock(return_value=(1, None))
        self._receiver.finish = MagicMock()
        self._receiver.do_POST()
        self._receiver.finish.assert_called()



