# coding= utf-8
import requests
from Utils.Property import Property


class InitConnect(object):
    def __init__(self):
        self.r = None
        self.base_url = Property.get_conf().get("serverconf", "server_url")
        self.port = Property.get_conf().get("serverconf", "port")

    # Send GET request.
    def send_get(self, url, parameter):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        if parameter:
            self.r = requests.get(http_url, params=parameter)
        else:
            self.r = requests.get(http_url)
        print (http_url)

    # Send POST request.
    def send_post(self, url, data):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print (http_url)
        self.r = requests.post(http_url, json=data)

    # Get response data.
    def get_data(self):
        result = None
        try:
            self.r.raise_for_status()
        except requests.RequestException as e:
            print(e)
            assert False
        else:
            result = self.r.json()
        return result

    # Get the GET request result.
    def get_result(self, url, parameter):
        self.send_get(url, parameter)
        response_data = self.get_data()
        return response_data

    # Get the POST request result.
    def post_result(self, url, data):
        self.send_post(url, data)
        response_data = self.get_data()
        return response_data

    # Get the cookie.
    def get_cookie(self):
        return self.r.json()["cookie"]

    # Get the token.
    def get_token(self):
        return self.r.json()["token"]

    # Get the cookie for the get request.
    def cookie_get(self, url, parameter):
        self.send_get(url, parameter)
        self.get_data()
        cookie = self.get_cookie()
        return cookie

    # Get the cookie for the post request.
    def cookie_post(self, url, data):
        self.send_post(url, data)
        self.get_data()
        cookie = self.get_cookie()
        return cookie

    # Get the token for the get request.
    def token_get(self, url, parameter):
        self.send_get(url, parameter)
        self.get_data()
        token = self.get_cookie()
        return token

    # Get the token for the post request.
    def token_post(self, url, data):
        self.send_post(url, data)
        self.get_data()
        token = self.get_token()
        return token
