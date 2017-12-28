from unittest import TestCase
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from iclientpy.rest.apifactory import APIFactory
from iclientpy.rest.api.management import *
import time


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