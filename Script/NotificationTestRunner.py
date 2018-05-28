# coding= utf-8
import os, time
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from HTMLTestRunner import HTMLTestRunner
from ParameterTestCase import ParameterTestCase
from Utils.Util import Util
from Script.NeoTestRunner import NeoTestRunner

if __name__ == '__main__':
    case_dir = os.path.join(Util.get_project_path(), "TestCases", "NeoCUTest", "NotificationAPITest")
    report_dir = os.path.join(Util.get_project_path(), "Report/Notification_Mail/")
    print report_dir
    suite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern="*Test.py", top_level_dir=None)
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = report_dir + now + '_result.html'
    fp = open(filename, 'wb')
    print discover
    runner = NeoTestRunner(stream=fp, title='Notification API Test Report', description='')
    runner.run(discover)
    fp.close()
