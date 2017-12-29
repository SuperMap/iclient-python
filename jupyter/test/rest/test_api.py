from unittest import TestCase, skip
from iclientpy.dtojson import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.api.management import *
import time
from typing import List
from iclientpy.rest.api.model import Feature


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        path = self.path # type:str
        try:
            if '/login' in path:
                self.send_response(201)
                self.send_header('Set-Cookie', 'JSESSIONID=958322873908FF9CA99B5CB443ADDD5C')
                self.end_headers()
                self.wfile.write(bytes('{"succeed":true,"referer":"/iserver/manager"}\n', encoding='utf8'))
            else:
                self.send_response(201)
                self.end_headers()
                self.wfile.write(bytes('[{"serviceType":"RESTMAP","serviceAddress":"http://127.0.0.1:8090/iserver/services/map-World/rest"}]\n', encoding='utf8'))
        except Exception:
            print(Exception)

server_running = threading.Condition()
running = False
httpd = HTTPServer(('127.0.0.1', 8091), Handler)
def run():
    global server_running, running
    with server_running:
        running = True
        server_running.notify_all()
    httpd.serve_forever()

server_thread = threading.Thread(target=run)

class TestAPI(TestCase):
    @classmethod
    def tearDownClass(cls):
        httpd.server_close()

    @skip("似乎在TeamCity上跑的时候挂起了")
    def test_post_workspace(self):
        global server_running, running
        server_thread.start();
        while not running:
            with server_running:
                server_running.wait(1)
        try:
            time.sleep(5) #MMP的，实在不知道怎么保证另一个线程里启动的http服务器启动了，我艹
            proxies = {
                # 'http': 'http://127.0.0.1:8888/'
            }
            facctory = APIFactory('http://127.0.0.1:8091/iserver', 'admin', 'iserver', proxies=proxies)
            mng = facctory.management()
            param = PostWorkspaceParameter()
            param.workspaceConnectionInfo = 'D:\packages\supermap_iserver_7.1.2_win64_zip\samples\data\World\World.sxwu'
            param.servicesTypes = [ServiceType.RESTMAP]
            time.sleep(2) # 还不知道怎么在Python上写支持并发的web服务器用于测试，所以，两次请求之间间隔2秒
            result = mng.postWorkspace(param=param)
            self.assertEqual(len(result), 1)
        except Exception:
            print(Exception)

    @skip('暂时只能在本地用本地服务跑，启动mock的http服务还存在问题')
    def test_post_feature(self):
            proxies = {
                'http': 'http://127.0.0.1:8888/'
            }
            facctory = APIFactory('http://127.0.0.1:8090/iserver', 'admin', 'iserver', proxies=proxies)
            data_service = facctory.data_service('data-World/rest')
            jsonstr = '[{"fieldNames":["SMID","SMSDRIW","SMSDRIN","SMSDRIE","SMSDRIS","SMUSERID","SMAREA","SMPERIMETER","SMGEOMETRYSIZE","SQKM","SQMI","COLOR_MAP","CAPITAL","COUNTRY","POP_1994","CONTINENT"],"fieldValues":["22","-7.433472633361816","62.35749816894531","-6.38972282409668","61.388328552246094","6","0.25430895154659083","5.743731026651685","4500","1474.69","569.38","5","示例首都a","示例国家a","47067.0","亚洲"],"geometry":{"id":22,"parts":[3],"points":[{"x":-40,"y":60},{"x":-45,"y":62},{"x":-40,"y":55},{"x":-40,"y":60}],"style":null,"type":"REGION"}},{"fieldNames":["SMID","SMSDRIW","SMSDRIN","SMSDRIE","SMSDRIS","SMUSERID","SMAREA","SMPERIMETER","SMGEOMETRYSIZE","SQKM","SQMI","COLOR_MAP","CAPITAL","COUNTRY","POP_1994","CONTINENT"],"fieldValues":["23","-7.433472633361816","62.35749816894531","-6.38972282409668","61.388328552246094","6","0.25430895154659083","5.743731026651685","4500","1474.69","569.38","5","示例首都b","示例国家b","47067.0","亚洲"],"geometry":{"id":23,"parts":[3],"points":[{"x":-40,"y":60},{"x":-45,"y":62},{"x":-40,"y":55},{"x":-40,"y":60}],"style":null,"type":"REGION","prjCoordSys":null}}]'
            features = from_json_str(jsonstr, List[Feature])
            result = data_service.postFeatures('World', 'Countries', features)
            self.assertTrue(result.succeed)
