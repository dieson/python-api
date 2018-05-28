# -*-coding:utf-8-*-
# @Time    : 2018/4/11 17:45
# @Author  : Zuo Ran
# @File    : NetworkQoSTest.py
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
class NetworkQoSTest(ParameterTestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "NetworkQoSData.json"))
    url = "/restapi/network/qoses/"
    connect = None

    @classmethod
    def setUpClass(cls):
        csrftoken = Certification().get_csrftoken()
        session_id = Certification().get_user_sessionid(csrftoken)
        cls.connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=cls.url)
        cls.networkMethod = NetworkAPI(cls.connect)

        tenantID = Info.get_tenant_id(cls.connect)
        cls.jsonData.write_specfic_data(tenantID, "post_network_qos_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "get_network_qos_id_01", "tenant_id")
        cls.jsonData.write_specfic_data(tenantID, "put_network_qos_id_01", "tenant_id")

    @ddt.data(*jsonData.next("get_network_qos_inspect_0"))
    def test_01_get_network_qos_inspect(self, data):
        print data["TestCase"]

        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/' % (self.url, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("post_network_qos_0"))
    def test_02_post_network_qos(self, data):
        print data["TestCase"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.post_result(self.url, inputdata)
        Util.assert_data(outputdata, responsedata)

        qosID = Util.get_value(responsedata, "id")
        self.jsonData.write(qosID, "put_network_qos_id_0", "qos_id")
        self.jsonData.write(qosID, "put_network_qos_id_0", "id")
        self.jsonData.write(qosID, "get_network_qos_id_0", "qos_id")
        self.jsonData.write(qosID, "get_network_qos_id_0", "id")
        self.jsonData.write(qosID, "get_network_qos_id_inspect_0", "qos_id")
        self.jsonData.write(qosID, "get_network_qos_id_devices_0", "qos_id")
        self.jsonData.write(qosID, "delete_network_qos_id_0", "qos_id")

    @ddt.data(*jsonData.next("put_network_qos_id_0"))
    def test_03_put_network_qos_id(self, data):
        print data["TestCase"]
        qosID = data["qos_id"]
        inputdata = data["input"]
        outputdata = data["output"]
        print self.connect.get_result('%s%s/%s/' % (self.url, qosID, "inspect"), {"method": "put"})
        responsedata = self.connect.put_result('%s%s/' % (self.url, qosID), inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_qos_id_0"))
    def test_04_get_network_qos_id(self, data):
        print data["TestCase"]
        qosID = data["qos_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result("%s%s/" % (self.url, qosID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_qos_id_inspect_0"))
    def test_05_get_qos_id_inspect(self, data):
        print data["TestCase"]
        qosID = data["qos_id"]
        inputdata = data["input"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, qosID, "inspect"), parameter=inputdata)
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_qos_id_devices_0"))
    def test_06_get_network_qos_id_devices(self, data):
        print data["TestCase"]
        qosID = data["qos_id"]
        outputdata = data["output"]

        responsedata = self.connect.get_result('%s%s/%s/' % (self.url, qosID, "qos_devices"))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("delete_network_qos_id_0"))
    def test_07_delete_network_qos_id(self, data):
        print data["TestCase"]
        qosID = data["qos_id"]
        outputdata = data["output"]

        responsedata = self.connect.delete_result('%s%s/' % (self.url, qosID))
        Util.assert_data(outputdata, responsedata)

    @ddt.data(*jsonData.next("get_network_qos_0"))
    def test_08_get_network_qos(self, data):
        print data["TestCase"]
        outputdata = data["output"]

        responsedata = self.connect.get_result(self.url)
        Util.assert_data_type_value(outputdata, responsedata)


if __name__ == '__main__':
    suite = ParameterTestCase.parametrize(NetworkQoSTest)
