# -*-coding:utf-8-*-
# @Time    : 2018/4/16 10:02
# @Author  : Zuo Ran
# @File    : NetworkRoutersInterfacesTest.py
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
class NetworkRoutersInterfacesTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkRoutersInterfacesData.json"))
    url = "/restapi/network/routers/"
    connect = None
    networkMethod = None
    externalID = None
    externalSubnetID = None
    routerID = None
    privateID = None
    privateSubnetID = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)
        cls.networkMethod = NetworkAPI(cls.connect)

        tenantID = Info.get_tenant_id(cls.connect)
        cls.externalID = Util.get_value(cls.networkMethod.create_network_external(), "id")
        print cls.externalID
        cls.externalSubnetID = Util.get_value(cls.networkMethod.create_external_subnets(cls.externalID), "id")
        print cls.externalSubnetID
        cls.routerID = Util.get_value(
            cls.networkMethod.create_routers(tenantID, cls.externalID, cls.externalSubnetID), "id")
        print cls.routerID
        cls.privateID = Util.get_value(cls.networkMethod.create_network_private(tenantID), "id")
        print cls.privateID
        cls.privateSubnetID = Util.get_value(cls.networkMethod.create_private_subnets(cls.privateID), "id")
        print cls.privateSubnetID

        cls.jsonData.write_specfic_data(tenantID, "post_network_routers_interfaces_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_routers_interfaces_01", "tenant_id")
        cls.jsonData.write_specfic_data(cls.routerID, "post_network_routers_interfaces_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "get_network_routers_interfaces_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "get_network_routers_interfaces_subnet_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "delete_network_routers_interfaces_subnet_01", "router_id")
        cls.jsonData.write_specfic_data(cls.privateID, "post_network_routers_interfaces_01", "network_id")
        cls.jsonData.write_specfic_data(cls.privateID, "get_network_routers_interfaces_01", "network_id")
        cls.jsonData.write_specfic_data(cls.privateSubnetID, "post_network_routers_interfaces_01", "subnet_id")
        cls.jsonData.write_specfic_data(cls.privateSubnetID, "get_network_routers_interfaces_subnet_01", "subnet_id")
        cls.jsonData.write_specfic_data(cls.privateSubnetID, "get_network_routers_interfaces_subnet_01", "id")
        cls.jsonData.write_specfic_data(cls.privateSubnetID, "delete_network_routers_interfaces_subnet_01", "subnet_id")

    @ddt.data(*jsonData.next("post_network_routers_interfaces_0"))
    def test_01_post_network_routers_interfaces(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        routerID = data["router_id"]
        outputdata = data["output"]

        responsedata = self.connect.post_result('%s%s/interfaces/' % (self.url, routerID), data=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_interfaces_0"))
    def test_02_get_network_routers_interfaces(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/interfaces/' % (self.url, routerID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_routers_interfaces_subnet_0"))
    def test_03_delete_network_routers_interfaces_subnet(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        interfaceID = data["subnet_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/interfaces/%s/' % (self.url, routerID, interfaceID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_interfaces_subnet_0"))
    def test_04_get_network_routers_interfaces_subnet(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        interfaceID = data["subnet_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/interfaces/%s/' % (self.url, routerID, interfaceID))
        Util.assert_data(outputdata, responsedata)

    @classmethod
    def tearDownClass(cls):
        cls.networkMethod.delete_routers(cls.routerID)
        cls.networkMethod.delete_subnets(cls.privateSubnetID)
        time.sleep(1)
        cls.networkMethod.delete_network_private(cls.privateID)
        cls.networkMethod.delete_subnets(cls.externalSubnetID)
        time.sleep(1)
        cls.networkMethod.delete_network_external(cls.externalID)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(NetworkRoutersInterfacesTest)
