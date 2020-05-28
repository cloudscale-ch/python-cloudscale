import click

@click.group()
@click.pass_context
def flavor(ctx):
    ctx.obj.cloud_resource_name = "flavor"
    ctx.obj.headers = [
        'name',
        'vcpu_count',
        'memory_gb',
        'slug',
        'zones',
    ]

@flavor.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    cloudscale.cmd_list()
