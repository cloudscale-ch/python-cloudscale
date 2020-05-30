import click

@click.group()
@click.pass_context
def image(ctx):
    ctx.obj.cloud_resource_name = "image"
    ctx.obj.headers = [
        'name',
        'operating_system',
        'default_username',
        'slug',
    ]

@image.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    cloudscale.cmd_list()
