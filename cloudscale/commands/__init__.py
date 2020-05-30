import sys
import click
from ..util import to_table, to_pretty_json, tags_to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

OUTPUT_FORMATS = [
    'table',
    'json',
]

class CloudscaleCommand:

    def __init__(self, cloud_resource_name=None, api_token=None, profile=None, debug=False, output="table", headers=[]):
        try:
            self._client = Cloudscale(
                api_token=api_token,
                profile=profile,
                debug=debug
            )
        except CloudscaleException as e:
            click.echo(e, err=True)
            sys.exit(1)

        self._output = output

        self.cloud_resource_name = cloud_resource_name
        self.headers = headers

    def get_client_resource(self):
        return getattr(self._client, self.cloud_resource_name)

    def _format_output(self, response):
        if self._output == "json":
            return to_pretty_json(response)
        else:
            if isinstance(response, dict):
                response = [response]
            return to_table(response, self.headers)

    def cmd_list(self, filter_tag=None):
        try:
            response = self.get_client_resource().get_all(filter_tag)
            click.echo(self._format_output(response))
        except CloudscaleApiException as e:
            click.echo(e, err=True)
            sys.exit(1)

    def cmd_show(self, uuid):
        try:
            response = self.get_client_resource().get_by_uuid(uuid)
            click.echo(self._format_output(response))
        except CloudscaleApiException as e:
            click.echo(e, err=True)
            sys.exit(1)

    def cmd_create(self, **kwargs):
        try:
            if 'tags' in kwargs:
                try:
                    kwargs['tags'] = tags_to_dict(kwargs['tags'])
                except ValueError as e:
                    click.echo(e, err=True)
                    sys.exit(1)

            response = self.get_client_resource().create(**kwargs)
            click.echo(self._format_output(response))
        except CloudscaleApiException as e:
            click.echo(e, err=True)
            sys.exit(1)

    def cmd_update(self, uuid, tags, clear_tags, clear_all_tags, **kwargs):
        try:
            _tags = dict()
            if not clear_all_tags:
                response = self.get_client_resource().get_by_uuid(uuid=uuid)
                _tags = response.get('tags', dict()).copy()

                for k in clear_tags:
                    _tags.pop(k, None)

            if tags:
                try:
                    _tags.update(tags_to_dict(tags))
                except ValueError as e:
                    click.echo(e, err=True)
                    sys.exit(1)

            self.get_client_resource().update(
                uuid=uuid,
                tags=_tags,
                **kwargs,
            )
            response = self.get_client_resource().get_by_uuid(uuid=uuid)
            click.echo(self._format_output(response))
        except CloudscaleApiException as e:
            click.echo(e, err=True)
            sys.exit(1)

    def cmd_delete(self, uuid, force):
        try:
            response = self.get_client_resource().get_by_uuid(uuid)
            click.echo(self._format_output(response))
            if not force:
                click.confirm('Do you want to delete?', abort=True)
            self.get_client_resource().delete(uuid)
            click.echo("Deleted!")
        except CloudscaleApiException as e:
            click.echo(e, err=True)
            sys.exit(1)

    def cmd_act(self, action, uuid):
        try:
            getattr(self.get_client_resource(), action)(uuid)
            response = self.get_client_resource().get_by_uuid(uuid)
            click.echo(self._format_output(response))
        except CloudscaleApiException as e:
            click.echo(e, err=True)
            sys.exit(1)
