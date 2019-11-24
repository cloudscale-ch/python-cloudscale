from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

FLOATING_IP_RESP = {
    "href": "https://api.cloudscale.ch/v1/floating-ips/192.0.2.123",
    "created_at": "2019-05-29T13:18:42.505197Z",
    "network": "192.0.2.123/32",
    "ip_version": 4,
    "server": {
        "href": "https://api.cloudscale.ch/v1/servers/47cec963-fcd2-482f-bdb6-24461b2d47b1",
        "uuid": "47cec963-fcd2-482f-bdb6-24461b2d47b1",
        "name": "db-master"
    },
    "region": {
        "slug": "lpg"
    },
    "next_hop": "198.51.100.1",
    "reverse_ptr": "192.0.2.123.cust.cloudscale.ch",
    "tags": {}
}

@responses.activate
def test_floating_ip_get_all():
    network_id = "192.0.2.123"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/floating-ips',
        json=[FLOATING_IP_RESP],
        status=200)

    cloudscale = Cloudscale(api_token="token")
    floating_ips = cloudscale.floating_ip.get_all()
    assert floating_ips[0]['network'] == network_id + '/32'

    runner = CliRunner()
    result = runner.invoke(cli, [
        'floating-ip',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0

@responses.activate
def test_floating_ip_get_by_uuid():
    network_id = "192.0.2.123"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/floating-ips/' + network_id,
        json=FLOATING_IP_RESP,
        status=200)

    cloudscale = Cloudscale(api_token="token")
    floating_ip = cloudscale.floating_ip.get_by_uuid(uuid=network_id)
    assert floating_ip['network'] == network_id + '/32'

    runner = CliRunner()
    result = runner.invoke(cli, [
        'floating-ip',
        '-a', 'token',
        'show',
        '--network-id',
        network_id,
    ])
    assert result.exit_code == 0

@responses.activate
def test_floating_ip_delete():
    network_id = "192.0.2.123"
    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/floating-ips/' + network_id,
        status=204)

    cloudscale = Cloudscale(api_token="token")
    floating_ip = cloudscale.floating_ip.delete(uuid=network_id)
    assert floating_ip is None

    runner = CliRunner()
    result = runner.invoke(cli, [
        'floating-ip',
        '-a', 'token',
        'delete',
        '--network-id',
        network_id,
    ])
    assert result.exit_code == 0

@responses.activate
def test_floating_ip_create():
    ip_version = 4
    server_uuid = "47cec963-fcd2-482f-bdb6-24461b2d47b1"
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/floating-ips',
        json=FLOATING_IP_RESP,
        status=204)

    cloudscale = Cloudscale(api_token="token")
    cloudscale.floating_ip.create(
        ip_version=ip_version,
    )
    runner = CliRunner()
    result = runner.invoke(cli, [
        'floating-ip',
        '-a', 'token',
        'create',
        '--ip-version',
        ip_version,
        '--server-uuid',
        server_uuid,
    ])
    assert result.exit_code == 0

@responses.activate
def test_floating_ip_update():
    network_id = "192.0.2.123"
    reverse_ptr = "192.0.2.123.cust.cloudscale.ch"
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/floating-ips/' + network_id,
        json=FLOATING_IP_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/floating-ips/' + network_id,
        json=FLOATING_IP_RESP,
        status=200)

    cloudscale = Cloudscale(api_token="token")
    floating_ip = cloudscale.floating_ip.update(uuid=network_id, reverse_ptr=reverse_ptr)
    assert floating_ip['network'] == network_id + '/32'
    assert floating_ip['reverse_ptr'] == reverse_ptr

    runner = CliRunner()
    result = runner.invoke(cli, [
        'floating-ip',
        '-a', 'token',
        'update',
        '--network-id',
        network_id,
        '--reverse-ptr',
        reverse_ptr,
    ])
    assert result.exit_code == 0
