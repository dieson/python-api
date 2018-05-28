# -*-coding:utf-8-*-
# @Time    : 2018/4/13 14:42
# @Author  : Zuo Ran
# @File    : NetworkSecurityGroupRulesTest.py
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
class NetworkSecurityGroupRulesTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkSecurityGroupRulesData.json"))
    url = "/restapi/network/security_group_rules/"
    connect = None
    networkMethod = None
    securityGroupID = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)
        cls.networkMethod = NetworkAPI(cls.connect)

        tenantID = Info.get_tenant_id(cls.connect)
        cls.jsonData.write_specfic_data(tenantID, "post_network_security_group_rules_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_security_group_rule_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_security_group_rule_id_01", "tenant_id")
        cls.securityGroupID = cls.networkMethod.create_security_group(tenantID)["data"]["security_group"]["id"]
        print cls.securityGroupID
        cls.jsonData.write_specfic_data(cls.securityGroupID, "post_network_security_group_rules_01", "security_group_id")
        cls.jsonData.write_specfic_data(cls.securityGroupID, "put_network_security_group_rule_id_01", "security_group_id")
        cls.jsonData.write_specfic_data(cls.securityGroupID, "get_network_security_group_rule_id_01", "security_group_id")

    @ddt.data(*jsonData.next("get_network_security_group_rules_inspect_0"))
    def test_01_get_network_security_group_rules_inspect(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_security_group_rules_0"))
    def test_02_post_network_security_group_rules(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result(self.url, inputdata)
        Util.assert_data(outputdata, responsedata)

        security_group_rule_id = Util.get_value(responsedata, "id")
        self.jsonData.write(security_group_rule_id, "delete_network_security_group_rule_id_0", "security_group_rule_id")
        self.jsonData.write(security_group_rule_id, "put_network_security_group_rule_id_0", "security_group_rule_id")
        self.jsonData.write(security_group_rule_id, "put_network_security_group_rule_id_0", "id")
        self.jsonData.write(security_group_rule_id, "get_network_security_group_rule_id_0", "security_group_rule_id")
        self.jsonData.write(security_group_rule_id, "get_network_security_group_rule_id_0", "id")
        self.jsonData.write(security_group_rule_id, "get_network_security_group_rule_id_inspect_0", "security_group_rule_id")

    @ddt.data(*jsonData.next("put_network_security_group_rule_id_0"))
    def test_03_put_network_security_group_rule_id(self, data):
        print data["TestCase"]
        security_group_rule_id = data["security_group_rule_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.put_result('%s%s/' % (self.url, security_group_rule_id), inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_security_group_rule_id_0"))
    def test_04_get_network_security_group_rule_id(self, data):
        print data["TestCase"]
        security_group_rule_id = data["security_group_rule_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result("%s%s/" % (self.url, security_group_rule_id))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_security_group_rule_id_inspect_0"))
    def test_05_get_security_group_rule_id_inspect(self, data):
        print data["TestCase"]
        security_group_rule_id = data["security_group_rule_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, security_group_rule_id, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_security_group_rule_id_0"))
    def test_06_delete_network_security_group_rule_id(self, data):
        print data["TestCase"]
        security_group_rule_id = data["security_group_rule_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, security_group_rule_id))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_security_group_rule_0"))
    def test_07_get_network_security_group_rule(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result(self.url)
        Util.assert_data_type_value(outputdata, responsedata)

    @classmethod
    def tearDownClass(cls):
        cls.networkMethod.delete_security_group(cls.securityGroupID)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(NetworkSecurityGroupRulesTest)
