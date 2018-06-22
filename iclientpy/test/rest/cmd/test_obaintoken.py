import httpretty
from unittest import TestCase
import mock
from io import StringIO
from iclientpy.rest.cmd.obaintoken import main, convert_to_minutes


class TestObainToken(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    @httpretty.activate
    def test_obaintoken(self, mock_print: StringIO):
        httpretty.register_uri(httpretty.POST, 'http://192.168.20.158:8090/iserver/services/security/login.json',
                               status=201, set_cookie='JSESSIONID=958322873908FF9CA99B5CB443ADDD5C',
                               body='{"referer":"/iportal/","reason":null,"succeed":true}')
        httpretty.register_uri(httpretty.POST, 'http://192.168.20.158:8090/iserver/services/security/tokens.json',
                               body="tokenstr", status=200)
        main(
            r"-l http://192.168.20.158:8090/iserver -u admin -p iserver -c RequestIP -e 60d --ip 127.0.0.1 --referer referer".split(
                ' '))
        self.assertEqual(mock_print.getvalue(), 'tokenstr\n')

    def test_convert_minutes(self):
        self.assertEqual(convert_to_minutes('1'), 1)
        self.assertEqual(convert_to_minutes('2m'), 2)
        self.assertEqual(convert_to_minutes('1h'), 1 * 60)
        self.assertEqual(convert_to_minutes('1d'), 1 * 60 * 24)
        self.assertEqual(convert_to_minutes('1w'), 1 * 60 * 24 * 7)
        self.assertEqual(convert_to_minutes('1M'), 1 * 60 * 24 * 30)
        self.assertEqual(convert_to_minutes('1y'), 1 * 60 * 24 * 365)
