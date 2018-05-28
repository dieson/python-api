# -*-coding:utf-8-*-
# @Time    : 2018/4/13 10:35
# @Author  : Zuo Ran
# @File    : NetworkSecurityGroupsTest.py
import ddt
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from Utils.JSONDriver import JSONDriver
from Utils.Util import Util
from Utils.Info import Info
from Connect.Certification import Certification
from Connect.SeparationConnect import SeparationConnect
from Script.ParameterTestCase import ParameterTestCase
from SeparationAPI.NetworkAPI import NetworkAPI

@ddt.ddt
class NetworkSecurityGroupsTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkSecurityGroupsData.json"))
    url = "/restapi/network/security_groups/"
    connect = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)
        cls.networkMethod = NetworkAPI(cls.connect)

        tenantID = Info.get_tenant_id(cls.connect)
        cls.jsonData.write_specfic_data(tenantID, "post_network_security_groups_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_security_group_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_security_group_id_01", "tenant_id")

    @ddt.data(*jsonData.next("get_network_security_groups_inspect_0"))
    def test_01_get_network_security_groups_inspect(self, data):
        print data["TestCase"]

        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_security_groups_0"))
    def test_02_post_network_security_groups(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result(self.url, inputdata)
        Util.assert_data(outputdata, responsedata)

        qosID = responsedata["data"]["security_group"]["id"]
        self.jsonData.write(qosID, "delete_network_security_group_id_0", "security_group_id")
        self.jsonData.write(qosID, "put_network_security_group_id_0", "security_group_id")
        self.jsonData.write(qosID, "put_network_security_group_id_0", "id")
        self.jsonData.write(qosID, "get_network_security_group_id_0", "security_group_id")
        self.jsonData.write(qosID, "get_network_security_group_id_0", "id")
        self.jsonData.write(qosID, "get_network_security_group_id_inspect_0", "security_group_id")
        self.jsonData.write(qosID, "get_network_security_group_id_devices_0", "security_group_id")

    @ddt.data(*jsonData.next("put_network_security_group_id_0"))
    def test_03_put_network_security_group_id(self, data):
        print data["TestCase"]
        security_group_id = data["security_group_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.put_result('%s%s/' % (self.url, security_group_id), inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_security_group_id_0"))
    def test_04_get_network_security_group_id(self, data):
        print data["TestCase"]
        security_group_id = data["security_group_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result("%s%s/" % (self.url, security_group_id))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_security_group_id_inspect_0"))
    def test_05_get_security_group_id_inspect(self, data):
        print data["TestCase"]
        security_group_id = data["security_group_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, security_group_id, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_security_group_id_devices_0"))
    def test_06_get_network_security_group_id_devices(self, data):
        print data["TestCase"]
        security_group_id = data["security_group_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, security_group_id, "security_group_devices"))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_security_group_id_0"))
    def test_07_delete_network_security_groups_id(self, data):
        print data["TestCase"]
        security_group_id = data["security_group_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, security_group_id))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_security_groups_0"))
    def test_08_get_network_security_groups(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result(self.url)
        Util.assert_data_type_value(outputdata, responsedata)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(NetworkSecurityGroupsTest)
