# encoding=utf-8
# @Time    : 2018/3/10 14:56
# @Author  : Zuo Ran
# @File    : NetworkAPI.py

import time
from Utils.Info import Info
from Connect.Certification import Certification
from Connect.SeparationConnect import SeparationConnect


class NetworkAPI(object):
    def __init__(self, connect):
        self.connect = connect

    def create_network_private(self, tenantID):
        """
        Create a private network
        :param tenantID: String
        :return: response
        """
        # Richard added for adopting different network types.
        private_network_type = self.get_private_network_type()
        print "Private network type is : %s" % private_network_type
        inputdata = {
            "network": {
                "tenant_id": tenantID,
                "name": "create_network_private",
                "shared": True
            }
        }
        if private_network_type == "vlan":
            inputdata["network"]["physical_network"] = self.get_private_physical_network()

        responsedata = self.connect.post_result("/restapi/network/private/", inputdata)
        return responsedata

    def delete_network_private(self, privateID):
        """
        Delete private network
        :param privateID:String
        """
        print self.connect.delete_result("/restapi/network/private/%s/" % privateID)

    # Richard Modified to adapting different external network types.
    def create_network_external(self):
        """
        Create a external network
        :return: response
        """
        physical_network = self.get_external_physical_network()
        inputdata = {
            "network": {
                "name": "external for testing",
                "admin_state_up": True,
                "physical_network": physical_network,
                "shared": True
            }
        }
        responsedata = self.connect.post_result("/restapi/network/external/", inputdata)
        return responsedata

    def delete_network_external(self, externalID):
        """
        Delete external network
        :param externalID: String
        """
        print self.connect.delete_result("/restapi/network/external/%s/" % externalID)

    def create_floating_ips(self, tenantID, externalID, subnetID):
        """
        Create the floating ip.
        :param tenantID: String
        :param externalID: String
        :param subnetID: String
        :return: response
        """
        # IP地址获取方式 - 自动
        inputdata = {
            "floatingip": {
                "tenant_id": tenantID,
                "floating_network_id": externalID,
                "subnet_id": subnetID,
                "description": "floating ip for testing"
            }
        }
        responsedata = self.connect.post_result("/restapi/network/floating_ips/", inputdata)
        return responsedata

    def delete_floating_ips(self, floatingIP):
        """
        Delete the floating ip.
        :param floatingIP: String
        """
        print self.connect.delete_result("/restapi/network/floating_ips/%s/" % floatingIP)

    def create_external_subnets(self, networkID):
        """
        Create the external subnet.
        :param networkID: String
        :return: response
        """
        inputdata = {
            "subnet": {
                "network_id": networkID,
                "name": "auto_external_subnet",
                "cidr": "192.168.199.0/24",
                "gateway_ip": "192.168.199.1",
                "enable_dhcp": True,
                "allocation_pools": "192.168.199.2,192.168.199.254",
                "dns_nameservers": "114.114.114.114",
                "host_routes": "10.6.6.0/24,10.5.5.1,10.7.7.0/24,10.5.5.1"
            }
        }
        responsedata = self.connect.post_result("/restapi/network/subnets/", inputdata)
        return responsedata

    def create_private_subnets(self, networkID):
        """
        Create the private subnet.
        :param networkID: String
        :return: response
        """
        inputdata = {
            "subnet": {
                "network_id": networkID,
                "name": "auto_subnet_testing",
                "cidr": "172.168.10.0/24",
                "gateway_ip": "172.168.10.1",
                "enable_dhcp": True,
                "allocation_pools": "172.168.10.2,172.168.10.254",
                "dns_nameservers": "114.114.114.114",
                "host_routes": "10.6.6.0/24,10.5.5.1,10.7.7.0/24,10.5.5.1"
            }
        }
        responsedata = self.connect.post_result("/restapi/network/subnets/", inputdata)
        return responsedata

    def delete_subnets(self, subnetsID):
        """
        delete the subnet.
        :param subnetsID: String
        """
        print self.connect.delete_result("/restapi/network/subnets/%s/" % subnetsID)

    def create_qoses_ingress(self, tenantID):
        """
        Create the qoses ingress.
        :param tenantID: String
        :return: response
        """
        inputdata = {
            "qos": {
                "tenant_id": tenantID,
                "name": "test_ingress",
                "description": "qoses for testing ",
                "type": "ratelimit",
                "shared": 1,
                "policies": {
                    "direction": "ingress",
                    "max_rate": "10000000"
                }
            }
        }
        responsedata = self.connect.post_result("/restapi/network/qoses/", inputdata)
        return responsedata

    def create_qoses_egress(self, tenantID):
        """
        Create the qos egress.
        :param tenantID: String
        :return: response
        """
        inputdata = {
            "qos": {
                "tenant_id": tenantID,
                "name": "test_egress",
                "description": "qoses for testing ",
                "type": "ratelimit",
                "shared": 1,
                "policies": {
                    "direction": "egress",
                    "max_rate": "10000000"
                }
            }
        }
        responsedata = self.connect.post_result("/restapi/network/qoses/", inputdata)
        return responsedata

    def delete_qoses(self, qosesID):
        """
        Delete the qos.
        :param qosesID: String
        """
        print self.connect.delete_result("/restapi/network/qoses/%s/" % qosesID)

    def create_security_group(self, tenantID):
        """
        Create the security group.
        :param tenantID: String
        :return: response
        """
        inputdata = {
            "security_group": {
                "tenant_id": tenantID,
                "name": "test",
                "description": "security group for testing"
            }
        }
        responsedata = self.connect.post_result("/restapi/network/security_groups/", inputdata)
        return responsedata

    def delete_security_group(self, securityGroupID):
        """
        Delete the security group
        :param securityGroupID: String
        """
        print self.connect.delete_result("/restapi/network/security_groups/%s/" % securityGroupID)

    def create_security_group_rules(self, tenantID, securityID):
        """
        Create the security group rule.
        :param tenantID: String
        :param securityID: String
        :return: response
        """
        inputdata = {
            "security_group_rule": {
                "tenant_id": tenantID,
                "security_group_id": securityID,
                "direction": "ingress",
                "protocol": "tcp",
                "ethertype": "IPv4",
                "port_range_max": 1901,
                "enabled": 1,
                "priority": 1,
                "port_range_min": 1900,
                "remote_ip_prefix": "192.168.1.0/24",
                "action": "accept"
            }
        }
        responsedata = self.connect.post_result("/restapi/network/security_group_rules/", inputdata)
        return responsedata

    def delete_security_group_rules(self, securityGroupRulesID):
        """
        Delete the security group rule.
        :param securityGroupRulesID: String
        """
        print self.connect.delete_result("/restapi/network/security_group_rules/%s/" % securityGroupRulesID)

    def create_routers(self, tenantID, networkID, subnetID):
        """
        Create the router.
        :param tenantID: String
        :param networkID: String
        :param subnetID: String
        :return: response
        """
        inputdata = {
            "router": {
                "tenant_id": tenantID,
                "name": "router_for_testing",
                "external_gateway_info": {
                    "network_id": networkID,
                    "external_fixed_ips": [
                        {
                            "subnet_id": subnetID
                        }
                    ]
                },
                "admin_state_up": True
            }
        }
        responsedata = self.connect.post_result("/restapi/network/routers/", inputdata)
        return responsedata

    def delete_routers(self, routersID):
        """
        Delete the router.
        :param routersID: String
        """
        print self.connect.delete_result("/restapi/network/routers/%s/" % routersID)

    def create_routers_ipsecs(self, routersID):
        """
        Create the router ipsec.
        :param routersID: String
        :return: response
        """
        # 未完成
        inputdata = {
            "peer_endpoint_group": {
                "name": "ipsecs for testing",
                "endpoints": ["192.1.1.12/32"]
            },
            "local_endpoint_group": {
                "name": "test",
                "endpoints": ["096124e6-67b1-480c-9329-16039f44fa33"]
            },
            "ipsec_site_connection": {
                "name": "ipsec_connection_1",
                "admin_state_up": True,
                "peer_address": "192.168.2.255",
                "peer_id": "192.168.2.255",
                "psk": "bla_bla_bla",
                "dpd": {
                    "action": "hold",
                    "interval": 40,
                    "timeout": 130
                },
                "mtu": 1600
            }
        }
        responsedata = self.connect.post_result("/restapi/network/routers/" + routersID + "/ipsecs/", inputdata)
        return responsedata

    def create_routers_interfaces(self, routersID, subnetID):
        """
        Create the router interface
        :param routersID: String
        :param subnetID: String
        :return: response
        """
        inputdata = {
            "subnet_id": subnetID
        }
        responsedata = self.connect.post_result("/restapi/network/routers/" + routersID + "/interfaces/", inputdata)
        return responsedata

    def delete_routers_interfaces(self, routersID, interfacesID):
        """
        Delete router interface
        :param routersID: String
        :param interfacesID: String
        """
        print self.connect.delete_result("/restapi/network/routers/%s/interfaces/%s/" % (routersID, interfacesID))

    def create_routers_portforwardings(self, routersID, externalID):
        """
        Create router portforwarding.
        :param routersID: String
        :param externalID: String
        :return: response
        """
        # 一对一
        inputdata = {
            "portforwardings":
                {
                    "inside_addr": externalID,
                    "protocol": "tcp",
                    "type": "one_to_one",
                    "start_port": 1,
                    "end_port": 1
                }
        }
        responsedata = self.connect.post_result("/restapi/network/routers/" + routersID + "/portforwardings/",
                                                inputdata)
        return responsedata

    def create_routers_openvpns(self, routersID, clientAddress):
        """
        Create the router open vpn.
        :param routersID: String
        :param clientAddress: String
        :return: response
        """
        inputdata = {
            "openvpn_connection":
                {
                    "client_address_pool_cidr": clientAddress,
                    "protocol": "udp",
                    "name": "openvpns for testing",
                    "limit_connections": 63,
                    "admin_state_up": True,
                    "port": 1194
                }
        }
        responsedata = self.connect.post_result("/restapi/network/routers/" + routersID + "/openvpns/", inputdata)
        return responsedata

    def delete_routers_openvpns(self, routersID, openvpnID):
        """
        Delete the router open vpns.
        :param routersID: String
        :param openvpnID: String
        """
        print self.connect.delete_result("/restapi/network/routers/%s/openvpns/%s/" % (routersID, openvpnID))

    def create_routers_pptps(self, routersID):
        """
        Create the router pptp
        :param routersID: String
        :return: response
        """
        inputdata = {
            "pptp_connection":
                {
                    "limit_connections": 253,
                    "admin_state_up": True,
                    "ip_address": "192.168.1.0/24"
                }
        }
        responsedata = self.connect.post_result("/restapi/network/routers/" + routersID + "/pptps/", inputdata)
        return responsedata

    def delete_routers_pptps(self, routersID, pptpID):
        """
        Delete the router pptp.
        :param routersID: String
        :param pptpID: String
        """
        self.connect.delete_result("/restapi/network/routers/%s/pptps/%s/" % (routersID, pptpID))

    def create_routers_pptps_users(self, routersID, pptpID):
        """
        Create user of router pptp
        :param routersID: String
        :param pptpID: String
        :return: response
        """
        inputdata = {
            "user":
                {
                    "username": "test",
                    "password": "passw0rd",
                }
        }
        responsedata = self.connect.post_result(
            "/restapi/network/routers/" + routersID + "/pptps/" + pptpID + "/users/", inputdata)
        return responsedata

    def create_routers_l2tps(self, routersID):
        """
        Create the routers l2tp
        :param routersID: String
        :return: response
        """
        inputdata = {
            "l2tp_connection":
                {
                    "psk": "test123",
                    "name": "l2tps for testing",
                    "admin_state_up": True,
                    "description": "test",
                    "net_cidr": "173.162.5.0/24"
                }
        }
        responsedata = self.connect.post_result("/restapi/network/routers/" + routersID + "/l2tps/", inputdata)
        return responsedata

    def delete_routers_l2tps(self, routersID, l2tpID):
        """
        Delete the router l2tp
        :param routersID: String
        :param l2tpID: String
        """
        print self.connect.delete_result("/restapi/network/routers/%s/l2tps/%s/" % (routersID, l2tpID))

    def create_routers_l2tps_users(self, routersID, pptpID):
        """
        Create user of router l2tp.
        :param routersID: String
        :param pptpID: String
        :return: response
        """
        inputdata = {
            "user":
                {
                    "username": "test",
                    "password": "passw0rd",
                }
        }
        responsedata = self.connect.post_result(
            "/restapi/network/routers/" + routersID + "/l2tps/" + pptpID + "/users/", inputdata)
        return responsedata

    def create_routers_gres(self, routersID, subnet):
        """
        Create the router gre
        :param routersID: String
        :param subnet: String
        :return: response
        """
        inputdata = {
            "gre_connection":
                {
                    "key": 564564,
                    "gre_remote_ip": "172.52.12.6",
                    "gre_local_ip": "172.52.12.4",
                    "description": "detail info",
                    "admin_state_up": True,
                    "remote_router_ip": "192.165.3.1",
                    "name": "gres for testing",
                    "gre_remote_subnet_addresses": [subnet]
                }
        }
        responsedata = self.connect.post_result("/restapi/network/routers/" + routersID + "/gres/", inputdata)
        return responsedata

    def delete_routers_gres(self, routersID, greID):
        """
        Delete the router gre
        :param routersID: String
        :param greID: String
        """
        print self.connect.delete_result("/restapi/network/routers/%s/gres/%s/" % (routersID, greID))

    # Richard added for creating private network by providing a name.
    def create_private_network_by_name(self, project_name, private_name, subnet_name, cidr):
        """
        Create the private network by name.
        :param project_name: String
        :param private_name: String
        :param subnet_name: String
        :param cidr:
        """
        private_network_type = self.get_private_network_type()
        project_id = Info.get_project_id_by_name_no_strikethrough(project_name)
        responsedata = None
        print "Private network type is : %s" % private_network_type
        if private_network_type == "vlan":
            physical_network = self.get_private_physical_network()
            inputdata = {
                "network": {
                    "tenant_id": project_id,
                    "name": private_name,
                    "physical_network": physical_network,
                    "shared": True
                }
            }
            responsedata = self.connect.post_result("/restapi/network/private/", inputdata)
        elif private_network_type == "vxlan":
            inputdata = {
                "network": {
                    "tenant_id": project_id,
                    "name": private_name,
                    "shared": True
                }
            }
            responsedata = self.connect.post_result("/restapi/network/private/", inputdata)
        if responsedata["code"] == 200:
            print "Create private network %s successfully." % private_name
            network_id = responsedata["data"]["network"]["id"]
            subnet_inputdata = {
                "subnet": {
                    "network_id": network_id,
                    "name": subnet_name,
                    "cidr": cidr,
                    "tenant_id": project_id
                }
            }
            subnet_responsedata = self.connect.post_result("/restapi/network/subnets/", subnet_inputdata)
            if subnet_responsedata["code"] == 200:
                print "Create subnet network %s successfully." % subnet_name
            else:
                print "Create subnet network %s failed." % subnet_name
        else:
            private_network = "Create private network %s failed." % private_name
            print private_network

    def get_external_network_type(self):
        responsedata = self.connect.get_result("/restapi/network/external/network_type/")
        external_network_type = responsedata["data"]["network_type"]
        return external_network_type

    def get_private_network_type(self):
        responsedata = self.connect.get_result("/restapi/network/private/network_type/")
        private_network_type = responsedata["data"]["network_type"]
        return private_network_type

    def get_private_physical_network(self):
        responsedata = self.connect.get_result("/restapi/network/private/physical_networks/")
        physical_network = responsedata["data"]["physical_networks"][0]
        return physical_network

    def get_external_physical_network(self):
        responsedata = self.connect.get_result("/restapi/network/external/physical_networks/")
        physical_network = responsedata["data"]["physical_networks"][0]
        return physical_network

    # This method only can be used in flat network mode.
    def get_external_network_id(self):
        responsedata = self.connect.get_result("/restapi/network/external/")
        external_network_info = responsedata["data"]["networks"][0]
        external_network_id = external_network_info["id"]
        return external_network_id

    def delete_provider_network(self):
        external_network_id = self.get_external_network_id()
        subnet_info = self.connect.get_result("/restapi/network/external/%s/" % external_network_id)
        subnet_id = subnet_info["data"]["network"]["subnets"][0]
        # delete subnet
        self.connect.delete_result("/restapi/network/subnets/%s/" % subnet_id)
        time.sleep(10)
        # delete provider_network
        self.connect.delete_result("/restapi/network/external/%s/" % external_network_id)
        time.sleep(10)

    def external_network_list(self):
        responsedata = self.connect.get_result("/restapi/network/external/")
        external_network_list = responsedata["data"]["networks"]
        return external_network_list

