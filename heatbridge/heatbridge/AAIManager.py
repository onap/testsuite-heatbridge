from collections import defaultdict

class AAIManager:
    """AAIManager manages the connection state and interaction between an aai instance and the heatbridge."""

    def __init__(self, context):
        self.openstack_context = context;

    def get_link(self, links, link_type):
        for link in links:
            if link['rel'] == link_type:
                return link['href'];

    def create_transactions(self, *args):
        transactions = defaultdict(list);
        for arg in args:
            transactions['transactions'].extend(arg);
        return transactions;

    def create_put(self, *args):
        put = defaultdict(list);
        put['put'].extend(args);
        return put;

    def create_vserver_put(self, server_info_dict, volumes_dict):
        #setup
        put = dict();
        body = dict();
        put['body'] = body;

        #required fields
        put['uri'] = "/cloud-infrastructure/cloud-regions/cloud-region/" + self.openstack_context.owner \
        + "/" + self.openstack_context.region + "/tenants/tenant/" + self.openstack_context.tenant \
        + "/vservers/vserver/" + server_info_dict['id'];
        body['vserver-id'] = server_info_dict['id'];
        body['vserver-name'] = server_info_dict['name'];
        body['vserver-name2'] = server_info_dict['name'];
        body['prov-status'] = server_info_dict['status'];
        body['vserver-selflink'] = self.get_link(server_info_dict['links'], "self");
        #body['in-maint'];
        #body['is-closed-loop-disabled'];
        #body['resource-version'];

        #optional fields
        volumes = []
        body['volumes'] = volumes
        for volume in volumes_dict:
            volumes.append(self.create_volume(volume));

        relations = [];
        if self.__exists(server_info_dict['metadata'], 'vnf_id'):
            data = self.__create_relationship_data("generic-vnf", "vnf-id", server_info_dict['metadata']['vnf_id']);
            list = self.__create_relationship_data_list(data);
            relations.append(self.__create_relationship("generic-vnf", list));
        if self.__exists(server_info_dict['flavor'], 'id'):
            data = self.__create_relationship_data("flavor", "flavor-id", server_info_dict['flavor']['id']);
            data2 = self.__create_relationship_data("cloud-region", "cloud-owner", self.openstack_context.owner);
            data3 = self.__create_relationship_data("cloud-region", "cloud-region-id", self.openstack_context.region);
            list = self.__create_relationship_data_list(data, data2, data3);
            relations.append(self.__create_relationship("flavor", list));
        if self.__exists(server_info_dict['image'], 'id'):
            data = self.__create_relationship_data("image", "image-id", server_info_dict['image']['id']);
            data2 = self.__create_relationship_data("cloud-region", "cloud-owner", self.openstack_context.owner);
            data3 = self.__create_relationship_data("cloud-region", "cloud-region-id", self.openstack_context.region);
            list = self.__create_relationship_data_list(data, data2, data3);
            relations.append(self.__create_relationship("image", list));
        body['relationship-list'] = self.__create_relationship_list(relations);
        return put

    def __create_relationship_list(self, items):
        rel_list = dict()
        relationship = []
        rel_list['relationship'] = relationship;
        relationship.extend(items);
        return rel_list;

    def __create_relationship_data_list(self, *relationship_data):
        relationship_data_list = [];
        relationship_data_list.extend(relationship_data);
        return relationship_data_list;

    def __create_relationship(self, related_to, relationship_data_list):
        relationship = dict();
        relationship['related-to'] = related_to;
        relationship['relationship-data'] = relationship_data_list
        return relationship;

    def __create_relationship_data(self, parent, key, value):
        relationship_data = dict();
        relationship_data['relationship-key'] = parent + "." + key;
        relationship_data['relationship-value'] = value;
        return relationship_data;

    def create_volume(self, volume_dict):
        #setup
        volume = dict()
        if 'volume' in volume_dict:
            volume['volume-id'] = volume_dict['volume']['id']
        #volume['volume-selflink']
        #volume['resource-version']
        #volume['relationship-list']
        return volume;

    def create_flavor_put(self, flavor_dict):
        #setup
        put = dict();
        body = dict()
        put['body'] = body

        #required fields
        put['uri'] = "/cloud-infrastructure/cloud-regions/cloud-region/" + self.openstack_context.owner \
        + "/" + self.openstack_context.region + "/flavors/flavor/" + flavor_dict['id']
        body['flavor-id'] = flavor_dict['id']
        body['flavor-name'] = flavor_dict['name']
        body['flavor-vcpus'] = flavor_dict['vcpus']
        body['flavor-ram'] = flavor_dict['ram']
        body['flavor-disk'] = flavor_dict['disk']
        if flavor_dict['OS-FLV-EXT-DATA:ephemeral'] != "":
            body['flavor-ephemeral'] = flavor_dict['OS-FLV-EXT-DATA:ephemeral']
        if flavor_dict['swap'] != "":
            body['flavor-swap'] = flavor_dict['swap']
        body['flavor-selflink'] = self.get_link(flavor_dict['links'], "self");
        #body['flavor-is-public'']
        #body['flavor-disabled']
        #body['relationship-list']
        return put

    def create_image_put(self, image_dict, server_info):
        #setup
        put = dict();
        body = dict()
        put['body'] = body
        put['uri'] = "/cloud-infrastructure/cloud-regions/cloud-region/" + self.openstack_context.owner \
        + "/" + self.openstack_context.region + "/images/image/" + image_dict['id']
        body['image-id'] = image_dict['id']
        body['image-name'] = image_dict['name']
        body['image-selflink'] = self.get_link(server_info['image']['links'], "bookmark");
        if self.__exists(image_dict, 'org.openstack__1__architecture'):
            body['image-architecture'] = image_dict['org.openstack__1__architecture']
        else:
            body['image-architecture'] = 'unknown'
        if self.__exists(image_dict, 'org.openstack__1__os_distro'):
            body['image-name'] = image_dict['org.openstack__1__os_distro']
        else:
            body['image-name'] = 'unknown'
        if self.__exists(image_dict, 'org.openstack__1__os_version'):
            body['image-os-version'] = image_dict['org.openstack__1__os_version']
        else:
            body['image-os-version'] = 'unknown'
        if self.__exists(image_dict, 'org.openstack__1__application_version'):
            body['application-version'] = image_dict['org.openstack__1__application_version']
        else:
            body['application-version'] = 'unknown'
        if self.__exists(image_dict, 'org.openstack__1__application_vendor'):
            body['application-vendor'] = image_dict['org.openstack__1__application_vendor']
        else:
            body['application-vendor'] = 'unknown'
        if self.__exists(image_dict, 'org.openstack__1__application'):
            body['application'] = image_dict['org.openstack__1__application']
        else:
            body['application'] = 'unknown'
        if self.__exists(image_dict, 'os_distro'):
            body['image-os-distro'] = image_dict['os_distro']
        else:
            body['image-os-distro'] = 'unknown'
        #body['metadata']
        #body['relationship-list'];
        return put

    def __exists(self, the_dict, key):
        if key in the_dict and the_dict[key] != "":
            return True;
        else:
            return False;

    def create_l_interface_put(self, port_dict, server_info_dict):
        #setup
        port = port_dict['port']
        put = dict();
        body = dict()
        put['body'] = body
        put['uri'] = "/cloud-infrastructure/cloud-regions/cloud-region/" + self.openstack_context.owner \
        + "/" + self.openstack_context.region + "/tenants/tenant/" + self.openstack_context.tenant \
        + "/vservers/vserver/" + port['device_id'] + "/l-interfaces/l-interface/" + port['name']
        body['interface-id'] = port['id']
        body['interface-name'] = port['name']
        body['macaddr'] = port['mac_address']
        #optional fields
        v4list = []
        v6list = []
        body['l3-interface-ipv4-address-list'] = v4list
        body['l3-interface-ipv6-address-list'] = v6list
        for ips in port['fixed_ips']:
            if '.' in ips['ip_address']:
                v4list.append(self.create_l3_interface_ipv4_address(port, ips));
            if ':' in ips['ip_address']:
                v6list.append(self.create_l3_interface_ipv6_address(port, ips));
        body['network-name'] = port['network_id']
        #body['selflink']
        #body['interface-role']
        #body['v6-wan-link-ip']
        #body['management-option']

        #optional fields
        return put

    def create_l3_interface_ipv4_address(self, port_dict, fixed_ip):
        #setup
        address = dict()
        address['l3-interface-ipv4-address'] = fixed_ip['ip_address']
        address['l3-interface-ipv4-prefix-length'] = '32'
        address['neutron-network-id'] = port_dict['network_id']
        address['neutron-subnet-id'] = fixed_ip['subnet_id']
        #address['vlan-id-inner']
        #address['vlan-id-outer']
        #address['is-floating']
        #address['relationship-list']
        return address;

    def create_l3_interface_ipv6_address(self, port_dict, fixed_ip):
        #setup
        address = dict()
        address['l3-interface-ipv6-address'] = fixed_ip['ip_address']
        address['l3-interface-ipv6-prefix-length'] = '128'
        address['neutron-network-id'] = port_dict['network_id']
        address['neutron-subnet-id'] = fixed_ip['subnet_id']
        #address['vlan-id-inner']
        #address['vlan-id-outer']
        #address['is-floating']
        #address['relationship-list']
        return address;

    def load_aai_data(self, request):
        return True;
