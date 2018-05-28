# -*-coding:utf-8-*-
# @Time    : 2018/4/18 17:02
# @Author  : Zuo Ran
# @File    : NetworkRoutersIpsecsTest.py
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
class NetworkRoutersIpsecsTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkRoutersIpsecsData.json"))
    url = "/restapi/network/routers/"
    connect = None
    networkMethod = None
    externalID = None
    externalSubnetID = None
    routerID = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)
        cls.networkMethod = NetworkAPI(cls.connect)

        tenantID = Info.get_tenant_id(cls.connect)
        print tenantID
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
        cls.networkMethod.create_routers_interfaces(cls.routerID, cls.privateSubnetID)

        cls.jsonData.write_specfic_data(tenantID, "post_network_routers_ipsecs_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_routers_ipsecs_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_routers_ipsecs_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(cls.routerID, "post_network_routers_ipsecs_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "get_network_routers_ipsecs_id_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "put_network_routers_ipsecs_id_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "delete_network_routers_ipsecs_id_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "get_network_routers_ipsecs_01", "router_id")
        cls.jsonData.write_specfic_data(cls.privateSubnetID, "post_network_routers_ipsecs_01", "local_endpoint_group",
                                        "endpoints")

    @ddt.data(*jsonData.next("post_network_routers_ipsecs_0"))
    def test_01_post_network_routers_ipsecs(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        routerID = data["router_id"]
        print routerID
        outputdata = data["output"]

        responsedata = self.connect.post_result('%s%s/ipsecs/' % (self.url, routerID), data=inputdata)
        time.sleep(10)

        ipsecsID = Util.get_value(responsedata, "id")
        self.jsonData.write(ipsecsID, "get_network_routers_ipsecs_id_0", "ipsecs_id")
        self.jsonData.write(ipsecsID, "put_network_routers_ipsecs_id_0", "ipsecs_id")
        self.jsonData.write(ipsecsID, "put_network_routers_ipsecs_id_0", "id")
        self.jsonData.write(ipsecsID, "delete_network_routers_ipsecs_id_0", "ipsecs_id")

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_ipsecs_id_0"))
    def test_02_get_network_routers_ipsecs_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        ipsecsID = data["ipsecs_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/ipsecs/%s/' % (self.url, routerID, ipsecsID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("put_network_routers_ipsecs_id_0"))
    def test_03_put_network_routers_ipsecs_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        ipsecsID = data["ipsecs_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.put_result('%s%s/ipsecs/%s/' % (self.url, routerID, ipsecsID), inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_routers_ipsecs_id_0"))
    def test_04_delete_network_routers_ipsecs_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        ipsecsID = data["ipsecs_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/ipsecs/%s/' % (self.url, routerID, ipsecsID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_ipsecs_0"))
    def test_05_get_network_routers_ipsecs(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/ipsecs/' % (self.url, routerID))
        Util.assert_data(outputdata, responsedata)

    @classmethod
    def tearDownClass(cls):
        cls.networkMethod.delete_routers_interfaces(cls.routerID, cls.privateSubnetID)
        cls.networkMethod.delete_routers(cls.routerID)
        cls.networkMethod.delete_subnets(cls.privateSubnetID)
        time.sleep(1)
        cls.networkMethod.delete_network_private(cls.privateID)
        cls.networkMethod.delete_subnets(cls.externalSubnetID)
        time.sleep(1)
        cls.networkMethod.delete_network_external(cls.externalID)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(ParameterTestCase)
