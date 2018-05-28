# -*-coding:utf-8-*-
# @Time    : 2018/3/10 13:47
# @Author  : Zuo Ran
# @File    : NetworkFloatingIpsTest.py
import os
import sys
import time

import ddt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from Utils.JSONDriver import JSONDriver
from Utils.Util import Util
from Utils.Info import Info
from Connect.Certification import Certification
from Connect.SeparationConnect import SeparationConnect
from Script.ParameterTestCase import ParameterTestCase
from SeparationAPI.NetworkAPI import NetworkAPI


@ddt.ddt
class NetworkSubnetsTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkSubnetsData.json"))
    url = "/restapi/network/subnets/"
    connect = None
    networkMethod = None
    privateID = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)
        cls.networkMethod = NetworkAPI(cls.connect)

        tenantID = Info.get_tenant_id(cls.connect)
        cls.privateID = Util.get_value(cls.networkMethod.create_network_private(tenantID), "id")
        print cls.privateID
        cls.jsonData.write_specfic_data(tenantID, "post_network_subnets_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_subnets_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_subnets_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(cls.privateID, "post_network_subnets_01", "network_id")
        cls.jsonData.write_specfic_data(cls.privateID, "get_network_subnets_id_01", "network_id")
        cls.jsonData.write_specfic_data(cls.privateID, "put_network_subnets_id_01", "network_id")

    @ddt.data(*jsonData.next("get_network_subnet_inspect_0"))
    def test_01_get_network_subnet_inspect(self, data):
        print data["TestCase"]

        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "inspect"), parameter=inputdata)
        print outputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_subnets_0"))
    def test_02_post_network_subnets(self, data):
        print data["TestCase"]

        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result(self.url, inputdata)
        print outputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

        subnetID = Util.get_value(responsedata, "id")
        self.jsonData.write(subnetID, "get_network_subnets_id_0", "subnet_id")
        self.jsonData.write(subnetID, "put_network_subnets_id_0", "subnet_id")
        self.jsonData.write(subnetID, "get_network_subnet_id_inspect_0", "subnet_id")
        self.jsonData.write(subnetID, "get_network_subnet_is_bind_router_0", "subnet_id")
        self.jsonData.write(subnetID, "delete_network_subnet_0", "subnet_id")

    @ddt.data(*jsonData.next("get_network_subnets_id_0"))
    def test_03_get_network_subnets_id(self, data):
        print data["TestCase"]

        subnetID = data["subnet_id"]
        outputdata = data["output"]
        responsedata = self.connect.get_result("%s%s/" % (self.url, subnetID))
        print responsedata
        print outputdata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("put_network_subnets_id_0"))
    def test_04_put_network_subnets_id(self, data):
        print data["TestCase"]

        subnetID = data["subnet_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.put_result('%s%s/' % (self.url, subnetID), inputdata)
        print responsedata
        print outputdata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_subnet_id_inspect_0"))
    def test_05_get_network_subnet_id_inspect(self, data):
        print data["TestCase"]

        subnetID = data["subnet_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, subnetID, "inspect"), parameter=inputdata)
        print outputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_subnet_is_bind_router_0"))
    def test_06_get_network_subnet_is_bind_router(self, data):
        print data["TestCase"]

        subnetID = data["subnet_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, subnetID, "is_bind_router"))
        print outputdata
        print responsedata

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_subnet_0"))
    def test_07_get_network_subnet(self, data):
        print data["TestCase"]

        outputdata = data["output"]

        responsedata = self.connect.get_result(self.url)
        print outputdata
        print responsedata

        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_subnet_0"))
    def test_08_delete_network_subnets(self, data):
        print data["TestCase"]

        subnetID = data["subnet_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, subnetID))
        print responsedata
        print outputdata

        Util.assert_data(outputdata, responsedata)

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
        cls.networkMethod.delete_network_private(cls.privateID)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(NetworkSubnetsTest)
