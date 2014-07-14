__author__ = 'thebvog'
__version__ = 'beta 0.2'

import socket
try:
    import urllib.request as urllib2
except:
    import urllib2
import json

class CodeForces:
    """
        CodeForces API class

        methods:
            # group of contest functions:
            getContestHacks(self, contestId)
            getContestList(self, gym=False, top=-1)
            getContestStandings(self, contestId, _from=-1, count=-1, handles=[], room=-1, showUnofficial=False)

            # group of problemset functions:
            getProblemSet(self, tags=[''])

            # group of user functions:
            getUserInfo(self, handles=['tourist'])
            getUserRatedList(self, top=-1, activeOnly=False)
            getUserRating(self, handle='tourist', top=-1)
            getUserStatus(self, handle='tourist', _from=1, count=1)

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
        try:
            response = urllib2.urlopen(request, timeout=16)
        except Exception:
            return None
        responseText = response.read()
        result = json.loads(responseText.decode('utf8'))
        if result['status'] == 'OK':
            return result['result']
        else:
            return None

    # group of contest functions
    def getContestHacks(self, contestId):
        apiFunction = 'contest.hacks?lang=%s&contestId=%d' % (self.apiLang, contestId)
        result = self._request(apiFunction)
        return result or False

    def getContestList(self, gym=False, top=-1):
        apiFunction = 'contest.list?lang=' + self.apiLang
        if gym:
            apiFunction += '&gym=true'
        result = self._request(apiFunction)
        if not result:
            return False
        if top > 0:
            result = result[0:top]
        return result

    def getContestStandings(self, contestId, _from=-1, count=-1, handles=[], room=-1, showUnofficial=False):
        """object of API response

            @param: contestId
                contestId in server, not a round number
            @param: _from
                start with 1, from this line return list
            @param: count
                number of lines in list
            @param: handles
                filter by this handles
            @param: room
                number of room, show standings only in room
            @param: showUnofficial
                obviously show unofficial participants too

            @return: object of API response
        """
        apiFunction = 'contest.standings?lang=%s&contestId=%d' % (self.apiLang, contestId)
        if _from > 0:
            apiFunction += '&from=%d' % (_from)

        if count > 0:
            apiFunction += '&count=%d' % (count)

        if handles:
            apiFunction += '&handles=%s' % (';'.join(handles))

        if room > 0:
            apiFunction += '&room=%d' % (room)

        if showUnofficial:
            apiFunction += '&showUnofficial=true'

        result = self._request(apiFunction)
        return result or False

    # group of problemset functions
    def getProblemSet(self, tags=['']):
        apiFunction = 'problemset.problems?lang=%s&tags=%s' % (self.apiLang, ';'.join(tags))
        result = self._request(apiFunction)
        return result or False

    # group of user functions
    def getUserInfo(self, handles=['tourist']):
        apiFunction = 'user.info?lang=%s&handles=%s' % (self.apiLang, ';'.join(handles))
        result = self._request(apiFunction)
        if not result:
            return False
        for key, value in enumerate(result):
            for color in self.userColors:
                if value['rating'] >= color['from'] and value['rating'] <= color['to']:
                    result[key]['color'] = color['value']
        return result

    def getUserRatedList(self, top=-1, activeOnly=False):
        apiFunction = 'user.ratedList?lang=%s' % (self.apiLang)
        if activeOnly:
            apiFunction += '&activeOnly=true'
        result = self._request(apiFunction)
        if not result:
            return False
        if top > 0:
            result = result[0:top]
        return result

    def getUserRating(self, handle='tourist', top=-1):
        apiFunction = 'user.rating?lang=%s&handle=%s' % (self.apiLang, handle)
        result = self._request(apiFunction)
        if not result:
            return False
        if top > 0:
            result = result[-top:0]
        return result

    def getUserStatus(self, handle='tourist', _from=1, count=1):
        apiFunction = 'user.status?lang=%s&handle=%s&from=%d&count=%d' % (self.apiLang, handle, _from, count)
        result = self._request(apiFunction)
        return result or False