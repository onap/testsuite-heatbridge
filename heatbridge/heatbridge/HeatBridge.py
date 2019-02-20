"""Module to provide Data from OpenStack to the AAI"""

import json
from heatbridge.OpenstackManager import OpenstackManager
from heatbridge.OpenstackContext import OpenstackContext
from heatbridge.AAIManager import AAIManager


class HeatBridge:
    """Heatbridge object used to sync OpenStack and AAI"""
    def __init__(self):
        self.openstack_manager = None
        self.aai_manager = None

    def init_bridge(self, openstack_identity_url, username, password, tenant,
                    region, owner, domain_id=None, project_name=None):
        """Initialization of the heatbridge"""
        self.openstack_manager = OpenstackManager(
            openstack_identity_url,
            OpenstackContext(username, password, tenant, region, owner,
                             domain_id, project_name))
        self.aai_manager = AAIManager(
            OpenstackContext(username, password, tenant, region,
                             owner, domain_id, project_name))

    def filterbyvalue(self, seq, key, value):
        """Filter by value function"""
        for elem in seq:
            if elem[key] == value:
                yield elem

    def build_request(self, heat_stack_id):
        """Request builder for Heatbridge
        Args:
            heat_stack_id: the id of the stack to sync to AAI
        """
        resources = self.openstack_manager.get_stack_resources(heat_stack_id)
        servers = list(self.filterbyvalue(
            resources, "resource_type", "OS::Nova::Server"))
        # networks =
        # list(self.filterbyvalue(resources,
        #                         "resource_type", "OS::Neutron::Net"))
        # subnets = list(self.filterbyvalue(resources,
        #                                   "resource_type",
        #                                   "OS::Neutron::Subnet"))
        ports = list(self.filterbyvalue(
            resources, "resource_type", "OS::Neutron::Port"))
        # keys = list(self.filterbyvalue(resources,
        #                                "resource_type",
        #                                "OS::Nova::KeyPair"))

        put_blocks = []

        # build the servers and attach them to vnf
        server_put_blocks = []
        image_put_blocks = []
        flavor_put_blocks = []
        for item in servers:
            server_info = self.openstack_manager.get_server_info(
                item['physical_resource_id'])
            server_volumes = self.openstack_manager.get_server_volumes(
                item['physical_resource_id'])
            volumes = []
            for vols in server_volumes:
                volumes.append(
                    self.openstack_manager.get_volume_info(vols['id']))
            aai_vserver = self.aai_manager.create_vserver_put(
                server_info, volumes)
            flavor_info = self.openstack_manager.get_flavor_info(
                server_info['flavor']['id'])
            aai_flavor = self.aai_manager.create_flavor_put(flavor_info)
            image_info = self.openstack_manager.get_image_info(
                server_info['image']['id'])
            aai_image = self.aai_manager.create_image_put(
                image_info, server_info)
            server_put_blocks.append(
                self.aai_manager.create_put(aai_vserver))
            image_put_blocks.append(
                self.aai_manager.create_put(aai_image))
            flavor_put_blocks.append(
                self.aai_manager.create_put(aai_flavor))
        put_blocks.extend(image_put_blocks)
        put_blocks.extend(flavor_put_blocks)
        put_blocks.extend(server_put_blocks)

        # build the ports and attach them to servers
        linterface_put_blocks = []
        # all servers have same vnf id
        random_server_info = self.openstack_manager.get_server_info(
            servers[0]['physical_resource_id'])
        for item in ports:
            # todo: pass in the networks from above
            port_info = self.openstack_manager.get_port_info(
                item['physical_resource_id'])
            aai_linterface = self.aai_manager.create_l_interface_put(
                port_info, random_server_info)
            linterface_put_blocks.append(
                self.aai_manager.create_put(aai_linterface))
        put_blocks.extend(linterface_put_blocks)

        return json.dumps(self.aai_manager.create_transactions(put_blocks))

    def bridge_data(self, heat_stack_id):
        """Bridge Data"""
        request = self.build_request(heat_stack_id)
        print(request)
        return request
