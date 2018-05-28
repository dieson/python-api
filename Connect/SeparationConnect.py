# encoding=utf-8
import requests
import time
from Utils.Property import Property


class SeparationConnect(object):
    def __init__(self, cookie=None, csrf=None, referer=None):
        self.r = None
        self.base_url = Property.get_conf().get("serverconf", "separation_server_url")
        self.port = Property.get_conf().get("serverconf", "separation_server_port")
        self.header = {}
        if csrf:
            self.header["X-CSRFtoken"] = csrf
        if referer:
            self.header["Referer"] = self.base_url + referer
        if cookie:
            self.header["cookie"] = "sessionid=" + cookie
        if csrf and cookie:
            self.header["cookie"] = "sessionid=" + cookie + ";csrftoken=" + csrf

    # Send GET request.
    def send_get(self, url, parameter):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        self.r = requests.get(http_url, params=parameter, headers=self.header, verify=False)
        print http_url

    # Send POST request.
    def send_post(self, url, data, files):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print http_url
        requests.packages.urllib3.disable_warnings()
        self.r = requests.post(http_url, json=data, headers=self.header, files=files, verify=False)
        time.sleep(1)

    # Send Delete request.
    def send_delete(self, url, data):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print http_url
        self.r = requests.delete(http_url, headers=self.header, json=data, verify=False)

    # Send PATCH request.
    def send_patch(self, url, data):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print http_url
        self.r = requests.patch(http_url, json=data, headers=self.header, verify=False)

    # Send PUT request.
    def send_put(self, url, data):
        http_url = '%s:%s%s' % (self.base_url, self.port, url)
        print http_url
        self.r = requests.put(http_url, json=data, headers=self.header, verify=False)

    # Get response data.
    def get_data(self):
        if self.r.status_code != 400 and self.r.status_code != 200:
            try:
                self.r.raise_for_status()
            except requests.RequestException as e:
                print e
                print self.r.content
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
    def post_result(self, url, data=None, files=None):
        self.send_post(url, data, files)
        response_data = self.get_data()
        return response_data

    # Get the POST request result.
    def delete_result(self, url, data=None):
        self.send_delete(url, data)
        response_data = self.get_data()
        return response_data

    # Get the PATCH request result.
    def patch_result(self, url, data=None):
        self.send_patch(url, data)
        response_data = self.get_data()
        return response_data

    # Get the PATCH request result.
    def put_result(self, url, data=None):
        self.send_put(url, data)
        response_data = self.get_data()
        return response_data

    def get_status_code(self):
        if self.r is None:
            return -1
        else:
            return self.r.status_code
