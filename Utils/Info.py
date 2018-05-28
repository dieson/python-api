# encoding=utf-8
# @Time    : 2018/3/5 10:56
# @Author  : Zuo Ran
# @File    : Info.py
import json
import requests
from Utils.Property import Property
from Utils.Util import Util


class Info(object):
    @staticmethod
    def _get_scoped_token():  # sunyu add this method to get a scoped token
        url = "%s:5000/v3/auth/tokens" % Property.get_conf().get("serverconf", "server_url")
        username = Property.get_conf().get("serverconf", "username")
        password = Property.get_conf().get("serverconf", "password")
        params = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": username,
                            "domain": {
                                "name": "Default"
                            },
                            "password": password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "admin",
                        "domain": {
                            "name": "Default"
                        }
                    }
                }
            }
        }
        try:
            r = requests.post(url, data=json.dumps(params))
            token = r.headers['X-Subject-Token']
        except requests.RequestException as e:
            token = None
            print e
        return token

    @staticmethod
    def get_project_id_by_name_no_strikethrough(project):
        token = Info._get_scoped_token()
        if token is not None:
            header = {"x-Auth-Token": token}
            url = "%s:5000/v3/projects" % Property.get_conf().get("serverconf", "server_url")
            r = requests.get(url, headers=header)
            for p in r.json()["projects"]:
                if p["name"] == project and len(p["id"]) > 20:
                    return p["id"]

    @staticmethod
    def get_project_id_by_name(project, format=True):  # added by sunyu, format to add hypen
        project_id = Info.get_project_id_by_name_no_strikethrough(project)
        if not format:
            return project_id
        return '-'.join(
            [project_id[0:8], project_id[8:12], project_id[12:16], project_id[16:20],
             project_id[20:]])

    @staticmethod
    def get_user_id_by_name(username, format=True):  # added by sunyu, format to add hypen
        token = Info._get_scoped_token()
        if token is not None:
            header = {"x-Auth-Token": token}
            url = "%s:5000/v3/users" % Property.get_conf().get("serverconf", "server_url")
            r = requests.get(url, headers=header)
            for p in r.json()["users"]:
                if p["name"] == username and len(p["id"]) > 20:
                    if not format :
                        return p["id"]
                    return '-'.join([p["id"][0:8], p["id"][8:12], p["id"][12:16], p["id"][16:20], p["id"][20:]])
            return ""

    @staticmethod
    def get_tenant_id(connect):
        url = "/restapi/company/project/"
        response = connect.get_result(url)
        return Util.get_value(response, "id")
