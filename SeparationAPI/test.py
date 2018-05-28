# encoding=utf-8
# @Time    : 2018/5/9 13:59
# @Author  : Zuo Ran
# @File    : test.py

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

# url = "/restapi/network/routers/"
#
# csrftoken = Certification().get_csrftoken()
# session_id = Certification().get_user_sessionid(csrftoken)
# connect = SeparationConnect(cookie=session_id, csrf=csrftoken, referer=url)
# networkMethod = NetworkAPI(connect)
#
# tenantID = Info.get_tenant_id(connect)
# print tenantID
# externalID = Util.get_value(networkMethod.create_network_external(), "id")
# print externalID
# externalSubnetID = Util.get_value(networkMethod.create_external_subnets(externalID), "id")
# print externalSubnetID
# routerID = Util.get_value(
#     networkMethod.create_routers(tenantID, externalID, externalSubnetID), "id")
# print routerID
# privateID = Util.get_value(networkMethod.create_network_private(tenantID), "id")
# print privateID
# privateSubnetID = Util.get_value(networkMethod.create_private_subnets(privateID), "id")
# print privateSubnetID
data = {"post_network_private_01":
    {
        "TestCase": "POST NETWORK PRIVATE",
        "input": {
            "network": {
                "shared": True,
                "tenant_id": "033c54f1743f4b00aaa4b9f66003acc3",
                "physical_network": "self",
                "name": "create_network_private",
                "segmentation_id": 250
            }
        }
    }
}
network = {
    "msg": "",
    "code": 200,
    "data": {
        "physical_networks": ["test"]
    }
}
# network["data"]["physical_networks"] = None
# print(network)

file_path = os.path.join(Util.get_project_path(), "Config", "license_file")
print file_path

def _change_value(data, value, *keys):
    firstKey = keys[0]
    if firstKey in data.keys():
        if len(keys) == 1:
            if type(data[firstKey]) is list:
                if type(value) is list:
                    data[firstKey] = value
                elif value is None:
                    data[firstKey] = value
                elif type(value) is not list:
                    del data[firstKey][:]
                    data[firstKey].append(value)
            elif type(data[firstKey]) is dict:
                data[firstKey].clear()
                data[firstKey].update(value)
            elif type(data[firstKey]) is not list and type(data[firstKey]) is not dict:
                data[firstKey] = value
        else:
            _change_value(data[firstKey], value, *keys[1:])
    else:
        for dataKey in data.keys():
            if type(data[dataKey]) is dict:
                # if firstKey in data[dataKey].keys():
                _change_value(data[dataKey], value, *keys)
            elif type(data[dataKey]) is list:
                for ar in data[dataKey]:
                    if type(ar) is dict:
                        _change_value(ar, value, *keys)
    return data


# print _change_value(network, None, "physical_networks")
