from .client import RestAPI
from .lib.server import Server
from .lib.server_group import ServerGroup
from .lib.volume import Volume
from .lib.flavor import Flavor
from .lib.floating_ip import FloatingIp
from .lib.image import Image
from .lib.region import Region
from .lib.network import Network
from .lib import CloudscaleApiException

__metaclass__ = type

__version__ = '0.0.1'

APP_NAME = 'cloudscale-cli'
CLOUDSCALE_API_ENDPOINT = 'https://api.cloudscale.ch/v1'

class CloudscaleException(Exception):
    pass

class Cloudscale:

    def __init__(self, api_token, verbose=False):

        if not api_token:
            raise CloudscaleException("Missing API key: see -h for help")

        self.api_token = api_token
        self.verbose = verbose
        self.service_classes = {
            'server': Server,
            'server_group': ServerGroup,
            'volume': Volume,
            'flavor': Flavor,
            'floating_ip': FloatingIp,
            'image': Image,
            'region': Region,
            'network': Network,
        }

    def __getattr__(self, name):
        try:
            client = RestAPI(
                api_token=self.api_token,
                endpoint=CLOUDSCALE_API_ENDPOINT
            )
            obj = self.service_classes[name]()
            obj._client = client
            obj.verbose = self.verbose
            return obj
        except NameError as e:
            raise CloudscaleException(e)
