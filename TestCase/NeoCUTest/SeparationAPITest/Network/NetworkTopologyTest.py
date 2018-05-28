# -*-coding:utf-8-*-
import ddt
import os
import sys
import unittest
from Utils.Util import Util

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from Utils.JSONDriver import JSONDriver
from Connect.Certification import Certification
from Connect.SeparationConnect import SeparationConnect
from Script.ParameterTestCase import ParameterTestCase


@ddt.ddt
class NetworkTopologyTest(ParameterTestCase):
    jsonData = JSONDriver("NeoCUData/SeparationData/NetworkTopologyData.json")
    url = "/restapi/network/topology/"
    connect = None

    @classmethod
    def setUpClass(cls):
        session_id = Certification().get_user_sessionid()
        cls.connect = SeparationConnect(cookie=session_id)

    @ddt.data(*jsonData.next("Get_NetworkTopology"))
    def test_get_network_topology(self, data):
        inputdata = data["input"]
        outputdata = data["output"]
        responsedata = self.connect.get_result(self.url, inputdata)
        print responsedata
        print outputdata

        Util.assert_data_type_value(outputdata, responsedata)


if __name__ == '__main__':
    unittest.main()
