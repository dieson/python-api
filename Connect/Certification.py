# encoding=utf-8

import json
import requests
from Utils.Property import Property


class Certification(object):
    def __init__(self):
        base_url = Property.get_conf().get("serverconf", "server_url")
        separation_url = Property.get_conf().get("serverconf", "separation_server_url")
        port = Property.get_conf().get("serverconf", "separation_server_port")
        self.authUrl = "%s:5000/v3/auth/tokens" % base_url
        self.separationUrl = "%s:%s/restapi/auth/userauth/login/" % (separation_url, port)
        self.username = Property.get_conf().get("serverconf", "username")
        self.password = Property.get_conf().get("serverconf", "password")
        self.regionurl = Property.get_conf().get("serverconf", "keystone_api_url")

    def get_xauth_headers(self):
        header = {"Content-type": "application/json", "Connection": "keep-alive"}
        data = {"auth": {"identity": {"methods": ["password"], "password": {
            "user": {"name": "%s" % self.username, "domain": {"id": "default"}, "password": "%s" % self.password}}}}}
        r = requests.post(self.authUrl, json=data, headers=header, verify=False)
        return r.headers

    def get_token(self):
        header = self.get_xauth_headers()
        return header["X-Subject-Token"]

    def get_csrftoken(self):
        data = {"username": self.username, "password": self.password}
        requests.packages.urllib3.disable_warnings()
        r = requests.post(self.separationUrl, json=data, verify=False)
        csrf_value = r.cookies.get("csrftoken")
        return csrf_value

    def get_user_sessionid(self, csrftoken=None):
        s = requests.Session()
        headers = {"Content-type": "application/x-www-form-urlencoded", "Referer": self.separationUrl,
                   "Cookie": "csrftoken=%s" % csrftoken}
        s.headers.update(headers)
        body = {"username": "%s" % self.username, "password": "%s" % self.password,
                "csrfmiddlewaretoken": u"%s" % csrftoken}
        requests.packages.urllib3.disable_warnings()
        s.request(method="post", url=self.separationUrl, data=body, verify=False)
        sessionid = s.cookies.get("sessionid")
        return sessionid
