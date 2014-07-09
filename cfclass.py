__author__ = 'thebvog'
__version__ = 'beta 0.1'

import socket
try:
    import urllib.request as urllib2
except:
    import urllib2
import json

class CodeForces:
    """
        CodeForces API class

    """

    def __init__(self, apiKey=None, apiLang='en'):
        self.apiHost = 'http://codeforces.ru/api/'
        self.apiKey = apiKey
        self.apiLang = apiLang
        self.userColors = [
            {'id': 0, 'from': 2601, 'to': 10000, 'value': '#ff0000'},
            {'id': 2, 'from': 2201, 'to': 2600, 'value': '#ff0000'},
            {'id': 4, 'from': 2051, 'to': 2200, 'value': '#bbbb00'},
            {'id': 6, 'from': 1901, 'to': 2050, 'value': '#ff8c00'},
            {'id': 8, 'from': 1701, 'to': 1900, 'value': '#aa00aa'},
            {'id': 10, 'from': 1501, 'to': 1700, 'value': '#0000ff'},
            {'id': 10, 'from': 1351, 'to': 1500, 'value': '#00ff00'},
            {'id': 12, 'from': 1201, 'to': 1350, 'value': '#00ff00'},
            {'id': 14, 'from': 0, 'to': 1200, 'value': '#808080'}
        ]

        # setup socket connection timeout
        timeout = 15
        socket.setdefaulttimeout(timeout)

    def _request(self, apiFunction='', proxy=None):
        # add proxy server
        if proxy:
            # sample: {'http': '127.0.0.1'}
            proxy = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)

        header = {
            'User-Agent': 'cfclass %s - Python CodeForces API (https://github.com/thebvog/cfclass)' % (__version__),
        }

        # send request to server
        request = urllib2.Request(self.apiHost + apiFunction, None, header)
        response = urllib2.urlopen(request)
        responseText = response.read()
        result = json.loads(responseText.decode('utf8'))
        if result['status'] == 'OK':
            return result['result']
        else:
            return None

    def getContestList(self, gym=False, top=-1):
        apiFunction = 'contest.list?lang=' + self.apiLang
        if gym == True:
            apiFunction += '&gym=true'
        result = self._request(apiFunction)
        if not result:
            return False
        if top > 0:
            result = result[0:top]
        return result

    def getUserInfo(self, handles=['turist']):
        apiFunction = 'user.info?lang=' + self.apiLang
        apiFunction += '&handles=' + ';'.join(handles)
        result = self._request(apiFunction)
        if not result:
            return False
        for key, value in enumerate(result):
            for color in self.userColors:
                if value['rating'] >= color['from'] and value['rating'] <= color['to']:
                    result[key]['color'] = color['value']
        return result