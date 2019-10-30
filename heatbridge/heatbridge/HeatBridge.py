import json
from OpenstackManager import OpenstackManager
from OpenstackContext import OpenstackContext
from AAIManager import AAIManager

class HeatBridge:
    def __init__(self):
        pass;

    def init_bridge(self, openstack_identity_url, username, password, tenant, region, owner, domain_id=None, project_name=None):
        self.om = OpenstackManager(openstack_identity_url, OpenstackContext(username, password, tenant, region, owner, domain_id, project_name));
        self.am = AAIManager(OpenstackContext(username, password, tenant, region, owner, domain_id, project_name));


    def filterbyvalue(self, seq, key, value):
        for el in seq:
            if el[key]==value: yield el

    def build_request(self, heat_stack_id):
        resources = self.om.get_stack_resources(heat_stack_id)
        servers = list(self.filterbyvalue(resources, "resource_type", "OS::Nova::Server"));
        #networks = list(self.filterbyvalue(resources, "resource_type", "OS::Neutron::Net"));
        #subnets = list(self.filterbyvalue(resources, "resource_type", "OS::Neutron::Subnet"));
        ports = list(self.filterbyvalue(resources, "resource_type", "OS::Neutron::Port"));
        #keys = list(self.filterbyvalue(resources, "resource_type", "OS::Nova::KeyPair"));

        put_blocks = []

        #build the servers and attach them to vnf
        server_put_blocks = []
        image_put_blocks = []
        flavor_put_blocks = []
        for item in servers:
            server_info = self.om.get_server_info(item['physical_resource_id']);
            server_volumes = self.om.get_server_volumes(item['physical_resource_id']);
            volumes = [];
            for vols in server_volumes:
                volumes.append(self.om.get_volume_info(vols['id']));
            aai_vserver = self.am.create_vserver_put(server_info, volumes);
            flavor_info = self.om.get_flavor_info(server_info['flavor']['id']);
            aai_flavor = self.am.create_flavor_put(flavor_info);
            image_info = self.om.get_image_info(server_info['image']['id']);
            aai_image = self.am.create_image_put(image_info, server_info);
            server_put_blocks.append(self.am.create_put(aai_vserver));
            image_put_blocks.append(self.am.create_put(aai_image));
            flavor_put_blocks.append(self.am.create_put(aai_flavor));
        put_blocks.extend(image_put_blocks);
        put_blocks.extend(flavor_put_blocks);
        put_blocks.extend(server_put_blocks);

        #build the ports and attach them to servers
        linterface_put_blocks = []
        #all servers have same vnf id
        random_server_info = self.om.get_server_info(servers[0]['physical_resource_id']);
        for item in ports:
            #todo: pass in the networks from above
            port_info = self.om.get_port_info(item['physical_resource_id'])
            aai_linterface = self.am.create_l_interface_put(port_info, random_server_info);
            linterface_put_blocks.append(self.am.create_put(aai_linterface));
        put_blocks.extend(linterface_put_blocks);

        return json.dumps(self.am.create_transactions(put_blocks));

    def bridge_data(self, heat_stack_id):
        request = self.build_request(heat_stack_id);
        print(request);
        return request;
