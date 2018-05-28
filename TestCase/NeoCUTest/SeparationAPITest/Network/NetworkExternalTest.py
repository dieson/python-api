# -*-coding:utf-8-*-
# @Time    : 2018/1/10 16:26
# @Author  : Zuo Ran
# @File    : NetworkExternalTest.py
import ddt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from Utils.JSONDriver import JSONDriver
from Utils.Util import Util
from Utils.Info import Info
from Connect.Certification import Certification
from Connect.SeparationConnect import SeparationConnect
from Script.ParameterTestCase import ParameterTestCase
import unittest


@ddt.ddt
class NetworkExternalTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkExternalData.json"))
    url = "/restapi/network/external/"
    connect = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)

    @ddt.data(*jsonData.next("get_external_network_type_01"))
    def test_01_get_external_network_type(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "network_type"))
        network_type = Util.get_value(responsedata, "network_type")

        self.jsonData.write(network_type, "post_network_external_0", "network_type")
        self.jsonData.write(network_type, "get_external_network_id_0", "network_type")
        self.jsonData.write(network_type, "put_external_network_id_0", "network_type")
        self.jsonData.write(network_type, "post_network_external_0", "provider:network_type")
        self.jsonData.write(network_type, "get_external_network_id_0", "provider:network_type")
        self.jsonData.write(network_type, "put_external_network_id_0", "provider:network_type")

        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_external_physical_networks_01"))
    def test_02_get_external_physical_networks(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "physical_networks"))
        physical_networks = Util.get_value(responsedata, "physical_networks")

        self.jsonData.write(physical_networks, "post_network_external_0", "physical_networks")
        self.jsonData.write(physical_networks, "get_external_network_id_0", "physical_networks")
        self.jsonData.write(physical_networks, "put_external_network_id_0", "physical_networks")
        self.jsonData.write(physical_networks, "post_network_external_0", "provider:physical_network")
        self.jsonData.write(physical_networks, "get_external_network_id_0", "provider:physical_network")
        self.jsonData.write(physical_networks, "put_external_network_id_0", "provider:physical_network")

        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_external_01"))
    def test_03_post_network_external(self, data):
        print data["TestCase"]

        tenantID = Info.get_project_id_by_name_no_strikethrough("admin")
        self.jsonData.write(tenantID, "post_network_external_0", "tenant_id")
        self.jsonData.write(tenantID, "get_external_network_id_0", "tenant_id")
        self.jsonData.write(tenantID, "put_external_network_id_0", "tenant_id")
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result(self.url, inputdata)

        networkID = Util.get_value(responsedata, "id")
        self.jsonData.write(networkID, "get_external_network_id_0", "id")
        self.jsonData.write(networkID, "get_external_network_id_0", "network_id")
        self.jsonData.write(networkID, "put_external_network_id_0", "id")
        self.jsonData.write(networkID, "put_external_network_id_0", "network_id")
        self.jsonData.write(networkID, "get_external_inspect_0", "network_id")
        self.jsonData.write(networkID, "delete_external_network_id_0", "network_id")

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_external_network_id_01"))
    def test_04_get_external_network_id(self, data):
        print data["TestCase"]
        network_id = data["network_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, network_id))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("put_external_network_id_01"))
    def test_05_put_external_network_id(self, data):
        print data["TestCase"]
        network_id = data["network_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.put_result('%s%s/' % (self.url, network_id), inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_external_inspect_01"))
    def test_06_get_external_inspect(self, data):
        print data["TestCase"]
        network_id = data["network_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, network_id, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_external_01"))
    def test_07_get_external(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result(self.url)
        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_external_network_id_01"))
    def test_08_delete_external_network_id(self, data):
        print data["TestCase"]
        network_id = data["network_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, network_id))
        Util.assert_data(outputdata, responsedata)


if __name__ == '__main__':
    unittest.main()
