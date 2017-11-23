from heatclient.v1.client import Client as HeatClient;
from novaclient.v2.client import Client as NovaClient;
from cinderclient.v1.client import Client as CinderClient;
from glanceclient.v2.client import Client as GlanceClient;
from neutronclient.v2_0.client import Client as NeutronClient;
import os_client_config
import logging

class OpenstackManager:
    """OpenstackManager manages the connection state and interaction between an openstack cloud and the heatbridge."""

    #this holds the session of the openstack clients
    __heat_client = None;
    __nova_client = None;
    __cinder_client = None;
    __glance_client = None;
    __neutron_client = None;
    __auth_resp = None;

    def __init__(self, identity_url, context):
        """ OpenstackManager

        `identity_url` Base identity_url of the identity server
        'context' Instance of OpenstackContext
        """
        self.openstack_context = context;
        self.identity_url = identity_url;
        self.authenticate(context.username, context.password, context.tenant, context.region)
        logging.basicConfig(level=logging.DEBUG)

    def authenticate(self, username, password, tenant, region):
        """ Authenticate to openstack env

        `username` username to authenticate to openstack

        `password` password to send

        `tenant` tenant to authenticate under

        `region` region to authenticate under
        """
        self.__heat_client = os_client_config.make_client('orchestration',
            auth_url=self.identity_url,
            username=username,
            password=password,
            project_id=tenant,
            region_name=region);
        self.__nova_client = os_client_config.make_client('compute',
            auth_url=self.identity_url,
            username=username,
            password=password,
            project_id=tenant,
            region_name=region);
        self.__cinder_client = os_client_config.make_client('volume',
            auth_url=self.identity_url,
            username=username,
            password=password,
            project_id=tenant,
            region_name=region);
        self.__glance_client = os_client_config.make_client('image',
            auth_url=self.identity_url,
            username=username,
            password=password,
            project_id=tenant,
            region_name=region);
        self.__neutron_client = os_client_config.make_client('network',
            auth_url=self.identity_url,
            username=username,
            password=password,
            project_id=tenant,
            region_name=region);
        #this next line is needed because for v2 apis that are after a certain release stopped providing version info in keytone url but rackspace did not
        self.__neutron_client.action_prefix = "";
        self.__auth_resp = True;

    def get_stack(self, stack_id):
        self.__check_authenticated()
        #: :type client: HeatClient
        client = self.__heat_client
        stack = client.stacks.get(stack_id)
        return stack.to_dict();

    def get_stack_resources(self, stack_id):
        self.__check_authenticated()
        #: :type client: HeatClient
        client = self.__heat_client;
        stack_resources =  client.resources.list(stack_id);
        stack_resources_dict = map(lambda x:x.to_dict(),stack_resources)
        return stack_resources_dict;

    def get_server_volumes(self, server_id):
        self.__check_authenticated()
        #: :type client: NovaClient
        client = self.__nova_client;
        server_volumes = client.volumes.get_server_volumes(server_id);
        server_volumes_dict = map(lambda x:x.to_dict(),server_volumes)
        return server_volumes_dict;

    def get_server_interfaces(self, server_id):
        self.__check_authenticated()
        #: :type client: NovaClient
        client = self.__nova_client;
        server_interfaces = client.virtual_interfaces.list(server_id);
        server_interfaces_dict = map(lambda x:x.to_dict(),server_interfaces)
        return server_interfaces_dict;

    def get_volume_info(self, volume_id):
        self.__check_authenticated()
        #: :type client: CinderClient
        client = self.__cinder_client;
        volume_info = client.volumes.get(volume_id);
        return volume_info.to_dict();

    def get_server_info(self, server_id):
        self.__check_authenticated()
        #: :type client: NovaClient
        client = self.__nova_client;
        server_info = client.servers.get(server_id);
        return server_info.to_dict();

    def get_image_info(self, image_id):
        self.__check_authenticated()
        #: :type client: GlanceClient
        client = self.__glance_client;
        image_info = client.images.get(image_id);
        return image_info;

    def get_flavor_info(self, flavor_id):
        self.__check_authenticated()
        #: :type client: NovaClient
        client = self.__nova_client;
        flavor_info = client.flavors.get(flavor_id);
        return flavor_info.to_dict();

    def get_port_info(self, port_id):
        self.__check_authenticated()
        #: :type client: NeutronClient
        client = self.__neutron_client;
        try:
            port_info = client.show_port(port_id);
        except Exception as e:
            client.action_prefix = "/v2.0";
            port_info = client.show_port(port_id);
        return port_info;

    def __check_authenticated(self):
        if self.__auth_resp == None:
            raise AssertionError('__auth_resp should exist before calling operation')