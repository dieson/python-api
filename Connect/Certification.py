# encoding=utf-8
from Utils.Property import Property
import pycurl
import json
import requests


class Certification(object):
    def __init__(self):
        base_url = Property.get_conf().get("serverconf", "server_url")
        separation_url = Property.get_conf().get("serverconf", "separation_server_url")
        self.authUrl = "%s:5000/v3/auth/tokens" % base_url
        self.separationUrl = "%s/auth/login/" % separation_url
        self.contents = ''
        self.username = Property.get_conf().get("serverconf", "username")
        self.password = Property.get_conf().get("serverconf", "password")
        self.regionurl = Property.get_conf().get("serverconf", "keystone_api_url")

    def store(self, buf):
        self.contents = "%s %s" % (self.contents, buf)

    '''override __str__'''

    def __str__(self):
        return self.contents

    def get_xauth_headers(self):
        retrieved_body = Certification()
        retrieved_headers = Certification()
        headers = {"Content-type": "application/json", "Connection": "keep-alive"}
        hdrs = ['%s: %s' % (str(k), str(v)) for k, v in headers.items()]
        body = {"auth": {"identity": {"methods": ["password"], "password": {
            "user": {"name": "%s" % self.username, "domain": {"id": "default"}, "password": "%s" % self.password}}}}}
        c = pycurl.Curl()
        c.setopt(pycurl.HTTPHEADER, hdrs)
        c.setopt(c.URL, self.authUrl)
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, json.dumps(body))
        c.setopt(c.WRITEFUNCTION, retrieved_body.store)
        c.setopt(c.HEADERFUNCTION, retrieved_headers.store)
        c.perform()
        s = retrieved_headers
        c.close()
        return s

    def get_token(self):
        header = str(Certification.get_xauth_headers(self))
        headerline = []
        for line in header.splitlines():
            headerline.append(line)
        tokenline = headerline[3]
        tl = tokenline.split(":")
        token = tl[1].strip()
        return token

    def get_csrftoken(self):
        requests.packages.urllib3.disable_warnings()
        r = requests.get(self.separationUrl, verify=False)
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


if __name__ == "__main__":
    c = Certification()
    print c.get_user_sessionid()
