# Example Usage in Python3

Hint: Use th CLI to get impression of the structure in JSON:

~~~shell
cloudscale-cli -o json ...
~~~

## List the slug of all flavors

~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
flavors = cloudscale.flavor.get_all()
for flavor in flavors:
    print(flavor['slug'])
~~~

## Listing

~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
servers = cloudscale.server.get_all()
for server in servers:
    if server['status'] == "running":
        print(server['name'])
~~~

### Use of filter_tag without value

~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
servers = cloudscale.server.get_all(filter_tag='project')
for server in servers:
    print(server['name'])
~~~

### Use of filter_tag with value

~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
servers = cloudscale.server.get_all(filter_tag='project=apollo')
for server in servers:
    print(server['name'])
~~~

## Get resource by UUID

~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

try:
    cloudscale = Cloudscale(api_token=api_token)
    server_group = cloudscale.server_group.get_by_uuid(uuid="5a1e5b28-d354-47a8-bfb2-01b048c20204")
    print(server_group['name'])
except CloudscaleApiException as e:
    print(e)
~~~

## Error handling

~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

try:
    cloudscale = Cloudscale(api_token=api_token)
    server = cloudscale.server.get_by_uuid(uuid="does-not-exist")
    print(server['name'])
except CloudscaleApiException as e:
    # Prints "API Response Error (404): Not found."
    print(e)
    # Prints "404"
    print(e.status_code)
    # Prints raw API response
    print(e.response)
~~~
