from iclientpy.rest.apifactory import iManagerAPIFactory
from iclientpy.rest.api.node_service import NodeService
import requests
from urllib.parse import quote
import logging


logger = logging.Logger(__name__)

class MsgHandler:
    def __init__(self, user_access_imgr_url, url, user, password, factory_kls = iManagerAPIFactory):
        self._url = url
        self._user_access_imgr_url = user_access_imgr_url
        to_portal_template = user_access_imgr_url + '/staticFiles/views/apps/iPortalDetail.html?id={id}'
        to_server_template = user_access_imgr_url + '/staticFiles/views/apps/iServerDetail2.html?id={id}'
        self._to_templates = {'iPortal': to_portal_template, 'iServer': to_server_template}
        self._access_href_template = user_access_imgr_url + '/security/sessionid?sessionid={sessionid}&to={to}'
        self._user = user
        self._password = password
        self._factory_kls = factory_kls
        self._cmds = {
            'list': self.do_list,
            'start': self.do_start,
            'stop': self.do_stop
        }

    def get_sessionid(self):
        response = requests.post(self._url + '/security/tokens.json', json={'username': self._user, 'password': self._password})
        response.raise_for_status()
        return response.cookies['JSESSIONID']

    def __call__(self, content:str, *args):
        try:
            content = content.strip()
            parts = content.split(' ', maxsplit=1)
            fun = self._cmds.get(parts[0].strip(), self.send_help)
            return fun(parts[1]) if len(parts) > 1 else fun()
        except:
            logger.exception('unknown error:' + content + ',' + str(args))
            return 'error'

    def send_help(self):
        return 'list/stop {id}/start {id}'

    def _get_node_service(self) -> NodeService:
        return self._factory_kls(base_url=self._url, username=self._user, passwd=self._password).node_service() # type:NodeService

    def do_list(self):
        node_s = self._get_node_service() # type:NodeService
        services = node_s.get_services().list
        msgs = []
        for service in services:
            is_online = node_s.get_current_M_PortTCP(service.id).get('value') == '1'
            status = '在线' if is_online else '离线'
            template = self._to_templates.get(service.type, None) # type:str
            if template is None:
                address = service.address
            else:
                to = template.format(id=service.id)
                to = quote(to, 'utf8')
                address = self._access_href_template.format(sessionid=self.get_sessionid(), to = to)
            msg = '{id}：{name}({type})-{status}-<a href="{address}">查看</a>'.format(id = service.id, name = service.name, type = service.type, status = status, address=address)
            msgs.append(msg)
        return '\n'.join(msgs) if len(msgs) != 0 else 'empty'

    def do_start(self, msg: str):
        node_s = self._get_node_service() # type:NodeService
        result = node_s.start_nodes([msg.strip()])
        return '启动{0}成功'.format(msg) if result.isSucceed else '启动{0}失败'.format(msg)

    def do_stop(self, msg):
        node_s = self._get_node_service() # type:NodeService
        result = node_s.stop_nodes([msg.strip()])
        return '停止{0}成功'.format(msg) if result.isSucceed else '停止{0}失败'.format(msg)


if __name__ == '__main__':
    from iclientpy.rest.cmd.wxreceiver.server import start_server
    import sys
    argv = [ MsgHandler(*(sys.argv[1:5]))]
    argv.extend(sys.argv[5:])
    start_server(*argv)