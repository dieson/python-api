# coding= utf-8
import os, time
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from HTMLTestRunner import HTMLTestRunner
from ParameterTestCase import ParameterTestCase
from Utils.Util import Util


if os.name == "nt":
    SUITE_DEFAULT_DIR = "d:\\mnt"
    CONF_DEFAULT_DIR = "c:\\tmp"
else:
    SUITE_DEFAULT_DIR = "/mnt/codedir/"
    CONF_DEFAULT_DIR = "/tmp" 


class NeoTestRunner(HTMLTestRunner):
    def __init__(self, conf=None, stream=sys.stdout, verbosity=1, title=None, description=None):

        super(NeoTestRunner, self).__init__(stream, verbosity, title, description)
        self.conf = conf
        self.suite = None
        
    def write_config(self):
        return self.conf

    def get_suite(self):
        suite = None
        suiteName = 'TestMe'
        suiteFile = 'TestMe.py'  # for test
        suiteType = 'API'
        suiteDir = None
        
        if self.conf is not None and self.conf['suiteType'] == '0' :
            suiteType = 'UI'
        if self.conf is not None and self.conf.has_key('suiteName'):
            suiteName = self.conf["suiteName"]
            suiteFile = os.sep.join([SUITE_DEFAULT_DIR, self.conf['productName'], suiteType, 
                                  suiteName + '.py'])
            suiteDir = os.sep.join([SUITE_DEFAULT_DIR, self.conf['productName'], suiteType])
            if not os.path.exists(suiteDir):
                print("Error: Directory %s does not exist" %suiteDir)
                return None
            
        if suiteDir is not None and not (suiteDir in sys.path):
            sys.path.insert(0, suiteDir) 
           
        loader = unittest.TestLoader()
        is_not_importable = False    
        try:
            print(suiteName)
            module = __import__(suiteName)
        except ImportError:
            is_not_importable = True
            print('Import error')
        else:
            tclass = getattr(module, suiteName)        
            suite = unittest.TestSuite()
            suite.addTest(ParameterTestCase.parametrize(tclass , param = self.conf))  
            return suite
        return None
                
    def get_result(self, suite):
        # Run the given test case or test suite.
        result = super(NeoTestRunner, self).run(suite)
        msgRc = {
            "passNum": -1, "failNum":-1, "errorNum": -1,
            "startTime": -1, "endTime": -1, "executeTime": -1, "reportPath": None
            }
        
        if result.success_count >= 0: 
            msgRc["passNum"] = result.success_count
        if result.failure_count >= 0:
            msgRc["failNum"] = result.failure_count
        if result.error_count >= 0:
            msgRc["errorNum"] = result.error_count
            
        msgRc["startTime"] = str(self.startTime)[:19]
        msgRc["endTime"] = str(self.startTime)[:19]
        deltaTime = float((self.stopTime - self.startTime).total_seconds())
        msgRc["executeTime"] = float('%.2f' %(deltaTime/60))
        
        return msgRc


if __name__ == '__main__':
    case_dir = os.path.join(Util.get_project_path(), "TestCases", "NeoCUTest", "SeparationAPITest")
    report_dir = os.path.join(Util.get_project_path(), "Report/SeparationAPI_Mail/")
    print report_dir
    #suite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern="*Test.py", top_level_dir=None)
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = report_dir + now + '_result.html'
    fp = open(filename, 'wb')
    print discover
    runner = NeoTestRunner(stream=fp, title='Separation API Test Report', description='')
    runner.run(discover)
    fp.close()

