# coding= utf-8
import os, time
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Utils.Util import Util
from Script.NeoTestRunner import NeoTestRunner
from Connect.Certification import Certification
from Connect.SeparationConnect import SeparationConnect
from SeparationAPI.ComputeAPI import ComputeAPI
from SeparationAPI.NetworkAPI import NetworkAPI


def add_test_cases_to_module(module_name, suite_name):
    """

    :param module_name: Test module name user want to add.
    :param suite_name: Test suite name for running.
    :return: nothing
    """
    module_dir = os.path.join(Util.get_project_path(), "TestCase", "NeoCUTest", "SeparationAPITest", "%s/" % module_name)
    module_suite = unittest.TestLoader().discover(module_dir, pattern="*Test.py", top_level_dir=None)
    suite_name.append(module_suite)

if __name__ == '__main__':

    # Initiate the session.
    url = "/restapi/compute/instances/"
    csrftoken = Certification().get_csrftoken()
    session_id = Certification().get_user_sessionid(csrftoken)
    connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=url)
    ca = ComputeAPI(connect)
    na = NetworkAPI(connect)
    private_network_name = "test_network"
    subnet_name = "test_subnet"
    instance_name = "test_vm"
    test_suite = []

    try:
        # Create "test_network" private network and "test_vm" instance.
        print "------ Start to create private network ------"
        na.create_private_network_by_name("demo", private_network_name, subnet_name, "12.12.12.0/24")
        print "------ Private network created ------"
        print "------ Start to create instance ------"
        ca.create_vm("demo", instance_name, "m1.medium", "centos7.2", "test_network", "default", "Test123")
        print "------ Instance created  ------"
        print "------ Wait for instance to active ------"
        active_status = ca.wait_for_instance_to_active(instance_name)
        if active_status is not True:
            print "Instance is not active"
            print "Compute, Storage and backup test cases skipped."
        else:
            print "------ Instance is now active ------"
            print "------ Adding Compute, Storage and Backup test cases. ------"
            add_test_cases_to_module("Compute", test_suite)
            add_test_cases_to_module("Volume", test_suite)

        external_network_type = na.get_external_network_type()
        if external_network_type == "vlan":
            print "------ Adding all bvt test cases. ------"
            # Add the test cases to test suite.
            add_test_cases_to_module("Alarm", test_suite)
            add_test_cases_to_module("DRS", test_suite)
            add_test_cases_to_module("Monitor", test_suite)
            add_test_cases_to_module("Network", test_suite)
            add_test_cases_to_module("Orchestra", test_suite)
            add_test_cases_to_module("Site", test_suite)
            add_test_cases_to_module("Statistics", test_suite)
        elif external_network_type == "flat":
            if na.external_network_list():
                na.delete_provider_network()
                if na.external_network_list():
                    print "------ Delete external network failed ------"
                    print "------Skipped Network Test Cases ------"
                    add_test_cases_to_module("Alarm", test_suite)
                    add_test_cases_to_module("DRS", test_suite)
                    add_test_cases_to_module("Monitor", test_suite)
                    add_test_cases_to_module("Orchestra", test_suite)
                    add_test_cases_to_module("Site", test_suite)
                    add_test_cases_to_module("Statistics", test_suite)
                else:
                    print "------ Default provider external network deleted. ------"
                    print "------ Adding all test cases. ------"
                    add_test_cases_to_module("Alarm", test_suite)
                    add_test_cases_to_module("DRS", test_suite)
                    add_test_cases_to_module("Monitor", test_suite)
                    add_test_cases_to_module("Network", test_suite)
                    add_test_cases_to_module("Orchestra", test_suite)
                    add_test_cases_to_module("Site", test_suite)
                    add_test_cases_to_module("Statistics", test_suite)
            else:
                print "------ External network is empty, adding all test cases. ------"
                add_test_cases_to_module("Alarm", test_suite)
                add_test_cases_to_module("DRS", test_suite)
                add_test_cases_to_module("Monitor", test_suite)
                add_test_cases_to_module("Network", test_suite)
                add_test_cases_to_module("Orchestra", test_suite)
                add_test_cases_to_module("Site", test_suite)
                add_test_cases_to_module("Statistics", test_suite)

        # Run the automation test cases.
        print "------ Now execute the API test cases ------"
        root_dir = os.path.join(Util.get_project_path(), "TestCase", "NeoCUTest", "SeparationAPITest/")
        loader = unittest.TestLoader()
        suite = loader.discover(root_dir, pattern="*Test.py", top_level_dir=None)
        report_dir = os.path.join(Util.get_project_path(), "Report/SeparationAPI_Mail/")
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        filename = report_dir + now + '_result.html'
        fp = open(filename, 'wb')
        runner = NeoTestRunner(stream=fp, title='Separation API Test Report', description='')
        runner.run(suite)
        fp.close()

    # If any error when running the test cases, exit 1 for Jenkins to mark as failure
    except Exception, e:
        print e.message
        sys.exit(1)

    finally:
        # tear down.
        print "------ Test Cases running complete ------"
        print "------ Start to tear down ------"
        ca.delete_vm_by_name(instance_name)
        time.sleep(5)
        network_id = ca.get_network_id_by_name(private_network_name)
        subnet_lists = ca.get_subnet_list_by_network_id(network_id)
        na.delete_subnets(subnet_lists[0])
        time.sleep(5)
        na.delete_network_private(network_id)
        print "------ Tear Down completed. ------"


