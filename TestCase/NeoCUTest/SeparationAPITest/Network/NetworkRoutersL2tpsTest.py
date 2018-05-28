# -*-coding:utf-8-*-
# @Time    : 2018/5/8 13:58
# @Author  : Zuo Ran
# @File    : NetworkRoutersl2tps.py
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
class NetworkRoutersL2tps(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkRoutersL2tpsData.json"))
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

        cls.jsonData.write_specfic_data(tenantID, "post_network_routers_l2tps_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_routers_l2tps_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_routers_l2tps_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "post_network_routers_l2tps_users_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "delete_network_routers_l2tps_user_01", "tenant_id")
        cls.jsonData.write_specfic_data(cls.routerID, "post_network_routers_l2tps_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "get_network_routers_l2tps_id_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "put_network_routers_l2tps_id_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "post_network_routers_l2tps_users_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "delete_network_routers_l2tps_user_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "delete_network_routers_l2tps_id_01", "router_id")
        cls.jsonData.write_specfic_data(cls.routerID, "get_network_routers_l2tps_01", "router_id")

    @ddt.data(*jsonData.next("post_network_routers_l2tps_0"))
    def test_01_post_network_routers_l2tps(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        routerID = data["router_id"]
        outputdata = data["output"]

        responsedata = self.connect.post_result('%s%s/l2tps/' % (self.url, routerID), data=inputdata)

        pptpID = Util.get_value(responsedata, "id")
        self.jsonData.write(pptpID, "get_network_routers_l2tps_id_0", "l2tp_id")
        self.jsonData.write(pptpID, "get_network_routers_l2tps_id_0", "id")
        self.jsonData.write(pptpID, "put_network_routers_l2tps_id_0", "l2tp_id")
        self.jsonData.write(pptpID, "put_network_routers_l2tps_id_0", "id")
        self.jsonData.write(pptpID, "post_network_routers_l2tps_users_0", "l2tp_id")
        self.jsonData.write(pptpID, "post_network_routers_l2tps_users_0", "id")
        self.jsonData.write(pptpID, "delete_network_routers_l2tps_user_0", "l2tp_id")
        self.jsonData.write(pptpID, "delete_network_routers_l2tps_user_0", "id")
        self.jsonData.write(pptpID, "delete_network_routers_l2tps_id_0", "l2tp_id")

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_l2tps_id_0"))
    def test_02_get_network_routers_l2tps_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        l2tpID = data["l2tp_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/l2tps/%s/' % (self.url, routerID, l2tpID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("put_network_routers_l2tps_id_0"))
    def test_03_put_network_routers_l2tps_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        l2tpID = data["l2tp_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        times = 0
        while "ACTIVE" is not \
                self.connect.get_result('%s%s/l2tps/%s/' % (self.url, routerID, l2tpID))["data"]["l2tp_connection"][
                    "status"] and times < 10:
            time.sleep(1)
            times += 1

        responsedata = self.connect.put_result('%s%s/l2tps/%s/' % (self.url, routerID, l2tpID), inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_routers_l2tps_users_0"))
    def test_04_post_network_routers_l2tps_users(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        l2tpID = data["l2tp_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result('%s%s/l2tps/%s/users/' % (self.url, routerID, l2tpID), data=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_routers_l2tps_user_0"))
    def test_05_delete_network_routers_l2tps_user(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        l2tpID = data["l2tp_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/l2tps/%s/users/' % (self.url, routerID, l2tpID), data=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_routers_l2tps_id_0"))
    def test_06_delete_network_routers_l2tps_id(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        l2tpID = data["l2tp_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/l2tps/%s/' % (self.url, routerID, l2tpID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_routers_l2tps_0"))
    def test_07_get_network_routers_l2tps(self, data):
        print data["TestCase"]
        routerID = data["router_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/l2tps/' % (self.url, routerID))
        Util.assert_data(outputdata, responsedata)

    @classmethod
    def tearDownClass(cls):
        cls.networkMethod.delete_routers(cls.routerID)
        time.sleep(1)
        cls.networkMethod.delete_subnets(cls.externalSubnetID)
        time.sleep(1)
        cls.networkMethod.delete_network_external(cls.externalID)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(ParameterTestCase)
