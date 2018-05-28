# -*-coding:utf-8-*-
# @Time    : 2018/4/10 16:54
# @Author  : Zuo Ran
# @File    : NetworkRoutersTest.py
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
class NetworkRoutersTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkRoutersData.json"))
    url = "/restapi/network/routers/"
    connect = None
    networkMethod = None
    externalID = None
    subnetID = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)
        cls.networkMethod = NetworkAPI(cls.connect)

        tenantID = Info.get_tenant_id(cls.connect)
        cls.externalID = Util.get_value(cls.networkMethod.create_network_external(), "id")
        print cls.externalID
        cls.subnetID = Util.get_value(cls.networkMethod.create_external_subnets(cls.externalID), "id")
        print cls.subnetID
        cls.jsonData.write_specfic_data(tenantID, "post_network_routers_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_routers_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_routers_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(cls.externalID, "post_network_routers_01", "network_id")
        cls.jsonData.write_specfic_data(cls.externalID, "get_network_routers_id_01", "network_id")
        cls.jsonData.write_specfic_data(cls.externalID, "put_network_routers_id_01", "network_id")
        cls.jsonData.write_specfic_data(cls.subnetID, "post_network_routers_01", "subnet_id")
        cls.jsonData.write_specfic_data(cls.subnetID, "get_network_routers_id_01", "subnet_id")
        cls.jsonData.write_specfic_data(cls.subnetID, "put_network_routers_id_01", "subnet_id")

    @ddt.data(*jsonData.next("get_network_routers_inspect_0"))
    def test_01_get_network_routers_inspect(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_routers_0"))
    def test_02_post_network_routers(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result(self.url, data=inputdata)

        routerID = Util.get_value(responsedata, "id")
        self.jsonData.write(routerID, "get_network_routers_id_0", "router_id")
        self.jsonData.write(routerID, "put_network_routers_id_0", "router_id")
        self.jsonData.write(routerID, "delete_network_routers_id_0", "router_id")

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_id_0"))
    def test_03_get_network_routers_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result("%s%s/" % (self.url, routerID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("put_network_routers_id_0"))
    def test_04_put_network_routers_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.put_result('%s%s/' % (self.url, routerID), inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_0"))
    def test_05_get_network_routers(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result(self.url)
        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_routers_id_0"))
    def test_06_delete_network_routers_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, routerID))

        Util.assert_data(outputdata, responsedata)

    @classmethod
    def tearDownClass(cls):
        cls.networkMethod.delete_subnets(cls.subnetID)
        time.sleep(1)
        cls.networkMethod.delete_network_external(cls.externalID)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(ParameterTestCase)
