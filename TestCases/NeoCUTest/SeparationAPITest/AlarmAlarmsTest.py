# -*-coding:utf-8-*-
# @Time    : 2017/11/6 14:43
# @Author  : Zuo Ran
# @File    : AlarmAlarmsTest.py
import unittest
import ddt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from Utils.JSONDriver import JSONDriver
from Utils.Util import Util
from Connect.Certification import Certification
from Connect.SeparationConnect import SeparationConnect


@ddt.ddt
class AlarmAlarmsTest(unittest.TestCase):
    jsonData = JSONDriver(os.path.join("NeoCUData", "SeparationData", "AlarmAlarmsData.json"))
    url = "/restapi/alarm/alarms/"
    connect = None

    @classmethod
    def setUpClass(cls):
        cookie = Certification().get_user_sessionid()
        cls.connect = SeparationConnect(cookie=cookie)

    @ddt.data(*jsonData.next("get_alarm_alarms"))
    def test_get_alarm_alarms(self, data):
        print data["TestCase"]
        inputData = data["input"]
        responseData = self.connect.get_result(self.url, inputData)
        outputData = data["output"]
        print inputData
        print responseData

        Util.assert_data_type_value(outputData, responseData)


if __name__ == '__main__':
    unittest.main()
