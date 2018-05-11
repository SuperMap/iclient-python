import httpretty
from unittest import TestCase
from iclientpy.rest.cmd.initserver import main


class TestInitiServer(TestCase):
    @httpretty.activate
    def test_initserver(self):
        httpretty.register_uri(httpretty.GET, 'http://192.168.20.158:8090/iserver/',
                               status=200)
        httpretty.register_uri(httpretty.PUT, 'http://192.168.20.158:8090/iserver/_setup.json',
                               status=204, set_cookie='JSESSIONID=958322873908FF9CA99B5CB443ADDD5C')
        httpretty.register_uri(httpretty.GET, 'http://192.168.20.158:8090/iserver/manager/license.json',
                               body='{"builder":{},"iServerChart":true,"iServerEnterprise":true,"iServerNetwork":true,"iServerPlot":true,"iServerProfessional":true,"iServerServiceNodeAddition":true,"iServerSituationEvolution":true,"iServerSpace":true,"iServerSpatial":true,"iServerSpatialProcessing":true,"iServerSpatialStreaming":true,"iServerStandard":true,"iServerTrafficTransfer":true,"trialVersion":false}',
                               status=200)
        httpretty.register_uri(httpretty.PUT, 'http://192.168.20.158:8090/iserver/_setup/enabledmodules.json',
                               status=204)
        httpretty.register_uri(httpretty.GET, 'http://192.168.20.158:8090/iserver/_initServer',
                               status=204)
        result = main(r"-l http://192.168.20.158:8090/iserver -u admin -p iserver ".split(' '))
        self.assertEqual(result, 0)
