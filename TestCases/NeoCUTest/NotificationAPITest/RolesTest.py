# -*-coding:utf-8-*-
# @Time    : 2017/10/27 9:49
# @Author  : Zuo Ran
# @File    : LogApiResultTest.py

import os
import sys
import ddt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from Utils.JSONDriver import JSONDriver
from Utils.Util import Util
from Connect.Certification import Certification
from Connect.Connect import Connect
from Script.ParameterTestCase import ParameterTestCase


@ddt.ddt
class RolesTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "NotificationAPIData", "RolesData.json"))
    url = "/api/v1/roles"
    connect = None

    @classmethod
    def setUpClass(cls):
        token = Certification().get_token()
        cls.connect = Connect(token=token)

    @ddt.data(*jsonData.next("post_roles"))
    def test_01_post_roles(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        responsedata = self.connect.post_result(self.url, inputdata)
        outputdata = data["output"]
        print inputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

        id = Util.get_dic_value(responsedata, "id")
        self.jsonData.write(id, "delete_roles_roleID", "roleID")
        self.jsonData.write(id, "get_roles", "id")
        self.jsonData.write(id, "get_roles_roleID", "roleID")
        self.jsonData.write(id, "get_roles_roleID", "id")
        self.jsonData.write(id, "patch_roles_roleID", "roleID")
        self.jsonData.write(id, "patch_roles_roleID", "id")

    @ddt.data(*jsonData.next("get_roles_0"))
    def test_02_get_roles(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        responsedata = self.connect.get_result(self.url, inputdata)
        outputdata = data["output"]
        print inputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_roles_roleID"))
    def test_03_get_roles_roleID(self, data):
        print data["TestCase"]
        inputdata = data["input"]["roleID"]
        responsedata = self.connect.get_result('%s/%s' % (self.url, inputdata))
        outputdata = data["output"]
        print outputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("patch_roles_roleID"))
    def test_04_patch_roles_roleID(self, data):
        print data["TestCase"]
        roleID = data["input"]["roleID"]
        inputdata = data["input"]["json"]
        responsedata = self.connect.patch_result('%s/%s' % (self.url, roleID), inputdata)
        outputdata = data["output"]
        print outputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_roles_roleID"))
    def test_05_delete_roles_roleID(self, data):
        print data["TestCase"]
        inputdata = data["input"]["roleID"]
        self.connect.send_delete('%s/%s' % (self.url, inputdata))

        self.assertEqual(self.connect.get_status_code(), 204)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(RolesTest)
