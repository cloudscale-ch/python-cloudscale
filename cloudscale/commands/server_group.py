import sys
import click
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

headers = ['name', 'type', 'servers', 'tags', 'uuid']


@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def server_group(ctx, profile, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token, profile, verbose)
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--filter-tag')
@server_group.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    try:
        response = cloudscale.server_group.get_all(filter_tag)
        if response:
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.argument('uuid', required=True)
@server_group.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.server_group.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--name', required=True)
@click.option('--type', 'group_type', default='anti-affinity', show_default=True)
@click.option('--tags', multiple=True)
@server_group.command("create")
@click.pass_obj
def cmd_create(cloudscale, name, group_type, tags):
    try:
        response = cloudscale.server_group.create(name, group_type, to_dict(tags))
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.argument('uuid', required=True)
@click.option('--name')
@click.option('--tags', multiple=True)
@server_group.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, tags):
    try:
        cloudscale.server_group.update(uuid, name, to_dict(tags))
        response = cloudscale.server_group.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.argument('uuid', required=True)
@click.option('--force', is_flag=True)
@server_group.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid, force):
    try:
        response = cloudscale.server_group.get_by_uuid(uuid)
        table = to_table([response], headers)
        click.echo(table)
        if not force:
            click.confirm('Do you want to delete?', abort=True)
        cloudscale.server_group.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
