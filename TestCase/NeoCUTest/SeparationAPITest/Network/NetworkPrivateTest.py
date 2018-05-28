# -*-coding:utf-8-*-
# @Time    : 2018/3/14 17:56
# @Author  : Zuo Ran
# @File    : NetworkPrivateTest.py
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
class NetworkPrivateTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkPrivateData.json"))
    url = "/restapi/network/private/"
    connect = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)

    @ddt.data(*jsonData.next("get_private_network_type_01"))
    def test_01_get_private_network_type(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "network_type"))
        network_type = Util.get_value(responsedata, "network_type")
        self.jsonData.write(network_type, "post_network_private_0", "provider:network_type")
        self.jsonData.write(network_type, "get_network_private_networkID_0", "provider:network_type")
        self.jsonData.write(network_type, "put_network_private_networkID_0", "provider:network_type")

        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_private_physical_networks_01"))
    def test_02_get_private_physical_networks(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "physical_networks"))
        physical_networks = Util.get_value(responsedata, "physical_networks")
        if physical_networks == ["self"]:
            self.jsonData.add(physical_networks, "post_network_private_0", "input", "network", "provider:physical_network")
        else:
            self.jsonData.delete("post_network_private_0", "input", "network", "provider:physical_network")
        self.jsonData.write(physical_networks, "post_network_private_0", "provider:physical_network")
        self.jsonData.write(physical_networks, "get_network_private_networkID_0", "provider:physical_network")
        self.jsonData.write(physical_networks, "put_network_private_networkID_0", "provider:physical_network")

        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_private_01"))
    def test_03_post_network_private(self, data):
        print data["TestCase"]

        tenantID = Info.get_tenant_id(self.connect)
        print tenantID
        self.jsonData.write(tenantID, "post_network_private_0", "tenant_id")
        self.jsonData.write(tenantID, "get_network_private_networkID_0", "tenant_id")
        self.jsonData.write(tenantID, "put_network_private_networkID_0", "tenant_id")
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result(self.url, inputdata)
        networkID = Util.get_value(responsedata, "id")
        self.jsonData.write(networkID, "get_network_private_networkID_0", "id")
        self.jsonData.write(networkID, "get_network_private_networkID_0", "network_id")
        self.jsonData.write(networkID, "put_network_private_networkID_0", "id")
        self.jsonData.write(networkID, "put_network_private_networkID_0", "network_id")
        self.jsonData.write(networkID, "get_private_inspect_0", "network_id")
        self.jsonData.write(networkID, "delete_network_private_networkID_0", "network_id")

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_private_networkID_01"))
    def test_04_get_network_private_networkID(self, data):
        print data["TestCase"]
        networkID = data["network_id"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, networkID))
        outputdata = data["output"]

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("put_network_private_networkID_01"))
    def test_05_put_network_private_networkID(self, data):
        print data["TestCase"]
        networkID = data["network_id"]
        inputdata = data["input"]

        responsedata = self.connect.put_result('%s%s/' % (self.url, networkID), data=inputdata)
        outputdata = data["output"]

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_private_inspect_01"))
    def test_06_get_private_inspect(self, data):
        print data["TestCase"]

        network_id = data["network_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, network_id, "inspect"), parameter=inputdata)

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_private_01"))
    def test_07_get_network_private(self, data):
        print data["TestCase"]

        responsedata = self.connect.get_result(self.url)
        outputdata = data["output"]

        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_private_networkID_01"))
    def test_08_delete_network_private_networkID(self, data):
        print data["TestCase"]
        networkID = data["network_id"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, networkID))
        outputdata = data["output"]

        Util.assert_data(outputdata, responsedata)


if __name__ == '__main__':
    unittest.main()
