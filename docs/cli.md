
# Command Line Interface

## Help

See all options:

~~~shell
 $ cloudscale-cli
Usage: cloudscale-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --version                  Show the version and exit.
  -a, --api-token TEXT       API token.
  -p, --profile TEXT         Profile used in config file.
  --debug                    Enables debug log output.
  -o, --output [table|json]  Output format.  [default: table]
  -h, --help                 Show this message and exit.

Commands:
  flavor
  floating-ip
  image
  network
  objects-user
  region
  server
  server-group
  subnet
  volume
~~~

## Autocompletion

zsh:

~~~shell
eval "$(_CLOUDSCALE_CLI_COMPLETE=source_zsh cloudscale-cli)"
~~~

bash:

~~~shell
eval "$(_CLOUDSCALE_CLI_COMPLETE=source cloudscale-cli)"
~~~

## Authentication

### Evironment variable

Using the ENV `CLOUDSCALE_API_TOKEN` variable:

~~~shell
export CLOUDSCALE_API_TOKEN=<your token>
cloudscale-cli flavor list
~~~

### Command line argument

Passing the `--api-token` parameter:

~~~shell
cloudscale-cli --api-token <your_token> server create ...
~~~

### Config file

Creating an ini file `.cloudscale.ini` (leading dot) in your `$HOME` or a `cloudscale.ini` (without leading dot) in the `CWD` with the following schema:

~~~ini
[default]
api_token = <token>
~~~

The default profile taken if available is `default`. The profile can be chosen by passing `--profile` or `CLOUDSCALE_PROFILE` ENV variable.

~~~shell
export CLOUDSCALE_PROFILE=staging
~~~

~~~ini
[production]
api_token = <token>

[staging]
api_token = <token>
~~~

Passing the command line option will overwrite the ENV var as one would expect:

~~~shell
cloudscale-cli --profile production server list
~~~

## Usage Examples

### Create Servers

Create one server:

~~~shell
cloudscale-cli server create \
--name my-server \
--flavor flex-2 \
--image centos-7 \
--ssh-key "$(cat ~/.ssh/id_rsa.pub)"
~~~

Create up to 10 servers in a row with `--count`:

!!! tip
    When using `--count`, the option `--name` allows to use string format syntax with 2 special variables:

    - `counter`: A number representing the current interation while creating multiple servers.
    - `uid`: A random 8 char/number long string.

    This allows to create dynamic names, e.g.:

    - Single number suffix: `--name 'myserver-{counter}'`
    - Number with leading zero suffix: `--name 'server-{counter:02d}'`
    - Random string suffix: `--name 'server-{uid}'`
    - Combinations: `--name 'server-{uid}-{counter:02d}.example.com'`

~~~shell
cloudscale-cli server create \
--name 'my-server-{uid}' \
--flavor flex-2 \
--image centos-7 \
--ssh-key "$(cat ~/.ssh/id_rsa.pub)" \
--count 10
~~~

### List Servers

Get a list as table view:

~~~shell
cloudscale-cli server list
~~~

Get a list as JSON response:

~~~shell
cloudscale-cli -o json server list
~~~

#### List Servers and Filter by Tag

List servers having the tag project with value gemini:

~~~shell
cloudscale-cli server list --filter-tag project=gemini
~~~

List servers having a tag project:

~~~shell
cloudscale-cli server list --filter-tag project
~~~

#### List Servers and Filter by JSON Query

Get a list of stopped servers:

~~~shell
cloudscale-cli server list --filter-json '[?status == `stopped`]'
~~~

Get a list of stopped servers having tag `project=demo` and start them after accepting:

~~~shell
cloudscale-cli server list \
--filter-tag project=demo \
--filter-json '[?status == `stopped`]' \
--action start
...
Do you want to start? [y/N]:
~~~

Start a list of stopped servers after accepting having tag `project=demo`:

~~~shell
cloudscale-cli server list \
--filter-tag project=demo \
--filter-json '[?status == `stopped`]' \
--action start
...
Do you want to start? [y/N]:
~~~

Delete a list of stopped servers after accepting having tag `project=demo`:

~~~shell
cloudscale-cli server list \
--filter-tag project=demo \
--filter-json '[?status == `stopped`]' \
--delete
...
Do you want to delete? [y/N]:
~~~

Get a simplified custom JSON list of stopped servers in profile `production`:

~~~shell
cloudscale-cli \
--output json \
--profile production \
server list \
--filter-json '[?status == `stopped`].{"server_name": name, "zone": zone.slug, "image": image.slug, "flavor": flavor.slug}'
[
    {
        "flavor": "flex-8",
        "image": "rhel-7",
        "server_name": "server1",
        "zone": "rma1"
    },
    {
        "flavor": "flex-8",
        "image": "centos-7",
        "server_name": "server2",
        "zone": "rma1"
    }
]
~~~

### Working with Tags

Add/Update servers tags (but keep all existing with different keys):

~~~shell
cloudscale-cli server update <uuid> --tag project=apollo --tag stage=prod
~~~

Delete a server tag (but keep all others existing):

~~~shell
cloudscale-cli server update <uuid> --clear-tag status
~~~

Add/Update server tags and remove a specific tag key:

~~~shell
cloudscale-cli server update <uuid> \
--tag project=apollo --tag stage=prod --clear-tag status
~~~

Add/Update server tags, remove other tags:

~~~shell
cloudscale-cli server update <uuid> \
--tag project=apollo --tag stage=prod --clear-all-tags
~~~

### Server Actions

Stop a server:

~~~shell
cloudscale-cli server stop <uuid>
~~~

Start a server:

~~~shell
cloudscale-cli server start <uuid>
~~~

Delete a server after accepting:

~~~shell
cloudscale-cli server delete <uuid>
~~~

Just delete without questions asked:

~~~shell
cloudscale-cli server delete -f <uuid>
~~~

## Verbosity and Debugging

Increase the verbosity by changing the log level from its default value `ERROR` to the value `INFO`:

~~~shell
cloudscale-cli --debug server list
~~~

or alternatively

~~~shell
export CLOUDSCALE_DEBUG=1
cloudscale-cli server list
~~~

To set the default log level e.g. to `DEBUG` use the `CLOUDSCALE_LOG_LEVEL` environment variable:

~~~shell
export CLOUDSCALE_LOG_LEVEL=debug
cloudscale-cli server list
~~~
