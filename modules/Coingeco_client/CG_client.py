from CG_exceptions import *

class Client(object):
    REST_API_URL = 'https://api.coingecko.com/api/v3/'
    def __init__(self):
        self.session = self._init_session()
    def _init_session(self):
        session = requests.Session()
        headers = {
            'Accepts': 'application/json'
        }
        session.headers.update(headers)
        return session
    def _additional_method_replace_char(self,parameters):    
        parameters = {x.replace('__', ""): v for x,v in parameters.items()}
        return parameters
    def _set_parameters(self, **kwargs):
        parameters = {}
        parameters.update(**kwargs)
        parameters = self._additional_method_replace_char(parameters)
        return parameters
    def _create_uri(self,path):
        return '{}{}'.format(self.REST_API_URL,path)
    def _request(self, method,path, **kwargs):       
        uri = self._create_uri(path)
        parameters = self._set_parameters(**kwargs)
        response = getattr(self.session, method)(uri, params=parameters)
        print(response)
        return self._handle_response(response)
    @staticmethod
    def _handle_response(response):
        """Internal helper for handling API responses from the Quoine server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status_code).startswith('2'):
            raise APIException(response)
        try:
            res = response.json()

            if 'code' in res and res['code'] != "200000":
                raise APIException(response)

            if 'success' in res and not res['success']:
                raise APIException(response)

            # by default return full response
            # if it's a normal response we have a data attribute, return that
            if 'data' in res:
                res = res['data']
            return res
        except ValueError:
            raise KucoinRequestException('Invalid Response: %s' % response.text)
          
    def _get(self,path, **kwargs):
        return self._request('get', path, **kwargs)
    def get_market_chart(self,currency, vs_currency, days):
        return self._get('coins/{}/market_chart'.format(currency), vs_currency=vs_currency, days=days)
    def get_market_chart_range(self,currency, vs_currency, timestamp_from, timestamp_to):
        return self._get('coins/{}/market_chart/range'.format(currency), vs_currency=vs_currency, from__=timestamp_from, to=timestamp_to)
    def get_coin_list(self):
        return self._get('coins/list')
    def get_coins_markets(self, vs_currency,price_change_percentage, ids='', category = '', order = '', per_page = '100', page = 1):   
        return self._get('coins/markets',vs_currency=vs_currency,
                         price_change_percentage=price_change_percentage,
                         ids=ids, category=category, order = order,
                         per_page = per_page, page = page)
    def get_ping(self):
        return self._get('ping')
    def get_search_trending(self):
        return self._get('search/trending')
    def get_derivatives(self, include_tickers='unexpired'):
        return self._get('derivatives')
    def get_exchanges(self,id):
        return self._get('exchanges/{}'.format(id))

if __name__ == '__main__':
    client = Client()
    #Get first 250 rows
    data = client.get_coins_markets('usd', '1h,24h,7d,14d,30d,200d,1y ', per_page = 250, page = 1)
