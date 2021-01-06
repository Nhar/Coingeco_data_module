from requests import Request, Session
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class APIException(Exception):
    """Exception class to handle general API Exceptions

        `code` values

        `message` format

    """
    def __init__(self, response):
        self.code = ''
        self.message = 'Unknown Error'
        try:
            json_res = response.json()
        except ValueError:
            self.message = response.content
        else:
            if 'error' in json_res:
                self.message = json_res['error']
            if 'msg' in json_res:
                self.message = json_res['msg']
            if 'message' in json_res and json_res['message'] != 'No message available':
                self.message += ' - {}'.format(json_res['message'])
            if 'code' in json_res:
                self.code = json_res['code']
            if 'data' in json_res:
                try:
                    self.message += " " + json.dumps(json_res['data'])
                except ValueError:
                    pass

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'APIException {}: {}'.format(self.code, self.message)      


if __name__ == '__main__':
    
    url = 'https://api.coingecko.com/api/v3/coins/nimiq-2/market_chart'
    parameters = {
      'vs_currency':'usd',
      'days':'30',
    }
    headers = {
      'Accepts': 'application/json'
    }

    session = Session()
    session.headers.update(headers)
    
    try:
      response = session.get(url, params=parameters)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    raise APIException(response)
