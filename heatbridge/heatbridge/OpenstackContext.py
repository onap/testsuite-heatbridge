class OpenstackContext:
    """OpenstackContext is a simple class that holds the provided information that heatbridge uses."""
    
    # this holds the info of the openstack clients
    username = None
    password = None
    tenant = None
    region = None
    owner = None
    domain_id = None
    project_name = None

    def __init__(self, username, password, tenant, region, owner, domain_id, project_name):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.region = region
        self.owner = owner
        self.domain_id = domain_id
        self.project_name = project_name
