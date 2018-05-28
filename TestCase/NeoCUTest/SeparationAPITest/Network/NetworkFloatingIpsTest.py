# -*-coding:utf-8-*-
# @Time    : 2018/3/7 13:47
# @Author  : Zuo Ran
# @File    : NetworkFloatingIpsTest.py
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
class NetworkFloatingIpsTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkFloatingIpsData.json"))
    url = "/restapi/network/floating_ips/"
    connect = None
    networkMethod = None
    externalID = None
    subnetID = None
    qosIngressID = None
    qoeEgressID = None

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
        cls.qosIngressID = Util.get_value(cls.networkMethod.create_qoses_ingress(tenantID), "id")
        cls.qoeEgressID = Util.get_value(cls.networkMethod.create_qoses_egress(tenantID), "id")
        qos = [cls.qosIngressID, cls.qoeEgressID]
        print qos
        cls.jsonData.write_specfic_data(tenantID, "post_network_floating_ips_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_floating_ips_floatingID_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_floating_ips_floatingID_01", "tenant_id")
        cls.jsonData.write_specfic_data(cls.externalID, "put_network_floating_ips_floatingID_01", "floating_network_id")
        cls.jsonData.write_specfic_data(cls.externalID, "post_network_floating_ips_01", "floating_network_id")
        cls.jsonData.write_specfic_data(cls.externalID, "get_network_floating_ips_floatingID_01", "floating_network_id")
        cls.jsonData.write_specfic_data(cls.subnetID, "post_network_floating_ips_01", "subnet_id")
        cls.jsonData.write_specfic_data(qos, "put_network_floating_ips_floatingID_01", "qos")

    @ddt.data(*jsonData.next("get_network_floating_ips_inspect_0"))
    def test_01_get_network_floating_ips_inspect(self, data):
        print data["TestCase"]

        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "inspect"), parameter=inputdata)

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_floating_ips_0"))
    def test_02_post_network_floating_ips(self, data):
        print data["TestCase"]

        inputdata = data["input"]
        outputdata = data["output"]
        responsedata = self.connect.post_result(self.url, inputdata)

        Util.assert_data(outputdata, responsedata)

        floatingID = Util.get_value(responsedata, "id")
        self.jsonData.write(floatingID, "get_network_floating_ips_floatingID_0", "floating_id")
        self.jsonData.write(floatingID, "get_network_floating_ips_floatingID_0", "id")
        self.jsonData.write(floatingID, "put_network_floating_ips_floatingID_0", "floating_id")
        self.jsonData.write(floatingID, "put_network_floating_ips_floatingID_0", "id")
        self.jsonData.write(floatingID, "delete_network_floating_ips_networkID_0", "floating_id")
        self.jsonData.write(floatingID, "get_network_floating_ips_id_devices_0", "floating_id")
        self.jsonData.write(floatingID, "get_network_floating_ips_id_inspect_0", "floating_id")
        print floatingID

    @ddt.data(*jsonData.next("get_network_floating_ips_floatingID_0"))
    def test_03_get_network_floating_ips_id(self, data):
        print data["TestCase"]

        floatingID = data["floating_id"]
        outputdata = data["output"]
        responsedata = self.connect.get_result("%s%s/" % (self.url, floatingID))

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("put_network_floating_ips_floatingID_0"))
    def test_04_put_network_floating_ips_id(self, data):
        #更新完成后返回的QOS为空
        print data["TestCase"]

        floatingID = data["floating_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.put_result('%s%s/' % (self.url, floatingID), inputdata)

        Util.assert_data(outputdata, responsedata)

    # 未获取到数据，待版本稳定后完善
    @ddt.data(*jsonData.next("get_network_floating_ips_id_devices_0"))
    def test_05_get_network_floating_ips_id_devices(self, data):
        print data["TestCase"]

        floatingID = data["floating_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, floatingID, "floating_ip_devices"))

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_floating_ips_id_inspect_0"))
    def test_06_get_network_floating_ips_id_inspect(self, data):
        print data["TestCase"]

        floatingID = data["floating_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, floatingID, "inspect"), parameter=inputdata)

        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_floating_ips_0"))
    def test_07_get_network_floating_ips(self, data):
        print data["TestCase"]

        outputdata = data["output"]

        responsedata = self.connect.get_result(self.url)

        Util.assert_data_type_value(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_floating_ips_networkID_01"))
    def test_08_delete_network_floating_ips(self, data):
        print data["TestCase"]

        floatingID = data["floating_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, floatingID))

        Util.assert_data(outputdata, responsedata)

    @classmethod
    def tearDownClass(cls):
        cls.networkMethod.delete_subnets(cls.subnetID)
        time.sleep(1)
        cls.networkMethod.delete_network_external(cls.externalID)
        cls.networkMethod.delete_qoses(cls.qoeEgressID)
        cls.networkMethod.delete_qoses(cls.qosIngressID)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(NetworkFloatingIpsTest)
