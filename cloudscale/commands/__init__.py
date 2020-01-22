import sys
import click
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

def _init(ctx, api_token, profile, verbose):
    try:
        ctx.obj = Cloudscale(api_token, profile, verbose)
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

def _list(resource, headers, filter_tag=None):
    try:
        response = resource.get_all(filter_tag)
        if response:
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

def _show(resource, uuid):
    try:
        response = resource.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

def _create(resource, **kwargs):
    try:
        if 'tags' in kwargs:
            kwargs['tags'] = to_dict(kwargs['tags'])
        response = resource.create(**kwargs)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

def _update(resource, uuid, tags, clear_tags, clear_all_tags, **kwargs):
    try:
        _tags = dict()
        if not clear_all_tags:
            server_group = resource.get_by_uuid(uuid=uuid)
            _tags = server_group['tags'].copy()
            for k in clear_tags:
                _tags.pop(k, None)

        if tags:
            _tags.update(to_dict(tags))

        resource.update(
            uuid=uuid,
            tags=_tags,
            **kwargs,
        )
        response = resource.get_by_uuid(uuid=uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

def _delete(resource, uuid, headers, force):
    try:
        response = resource.get_by_uuid(uuid)
        table = to_table([response], headers)
        click.echo(table)
        if not force:
            click.confirm('Do you want to delete?', abort=True)
        resource.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

def _act(resource, action, uuid):
    try:
        response = getattr(resource, action)(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
