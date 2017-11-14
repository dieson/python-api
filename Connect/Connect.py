# encoding=utf-8
import requests
from Utils.Property import Property


class Connect(object):
    def __init__(self, token=None, cookie=None):
        self.r = None
        self.base_url = Property.get_conf().get("serverconf", "server_url")
        self.port = Property.get_conf().get("serverconf", "port")
        self.header = {}
        if token or cookie:
            self.header["X-Auth-Token"] = token
            self.header["cookie"] = cookie

    # Send GET request.
    def send_get(self, url, parameter):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        if parameter:
            self.r = requests.get(http_url, params=parameter, headers=self.header)
        else:
            self.r = requests.get(http_url, headers=self.header)
        print (http_url)

    # Send POST request.
    def send_post(self, url, data):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print (http_url)
        self.r = requests.post(http_url, json=data, headers=self.header)

    # Send Delete request.
    def send_delete(self, url):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print http_url
        self.r = requests.delete(http_url, headers=self.header)

    # Send PATCH request.
    def send_patch(self, url, data):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print http_url
        self.r = requests.patch(http_url, json=data, headers=self.header)

    # Get response data.
    def get_data(self):
        try:
            self.r.raise_for_status()
        except requests.RequestException as e:
            print(e)
            assert False
        else:
            result = self.r.json()
            return result

    # Get the GET request result.
    def get_result(self, url, parameter=None):
        self.send_get(url, parameter)
        response_data = self.get_data()
        return response_data

    # Get the POST request result.
    def post_result(self, url, data):
        self.send_post(url, data)
        response_data = self.get_data()
        return response_data

    # Get the POST request result.
    def delete_result(self, url):
        self.send_delete(url)
        return self.r

    # Get the PATCH request result.
    def patch_result(self, url, data):
        self.send_patch(url, data)
        response_data = self.get_data()
        return response_data

    def get_status_code(self):
        if self.r is None:
            return -1
        else:
            return self.r.status_code
