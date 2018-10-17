
import click

from punica.asset.asset import Asset
from .main import main


@main.group('asset', invoke_without_command=True)
@click.pass_context
def asset_cmd(ctx):
    """
    manager your asset, transfer, balance, withdraw ong, unbound ong.
    """
    pass


@asset_cmd.command('transfer')
@click.option('--asset', nargs=1, type=str, default='', help='Asset of ONT or ONG (default: "ont")')
@click.option('--sender', nargs=1, type=str, default='', help='Transfer-out account <address>')
@click.option('--to', nargs=1, type=str, default='', help='Transfer-in account <address>')
@click.option('--amount', nargs=1, type=int, default=0, help='Transfer <amount>.int number')
@click.option('--gas_price', nargs=1, type=int, default=500, help='Gas price of transaction (default: 0)')
@click.option('--gas_limit', nargs=1, type=int, default=20000, help='Gas limit of the transaction (default: 20000)')
@click.option('--network', nargs=1, type=str, default='', help='which network will be used,default test network')
@click.pass_context
def transfer(ctx, asset, sender, to, amount, gas_price, gas_limit, network):
    """
    transfer your asset to another address.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Asset.transfer(project_dir, asset, sender, to, amount, gas_price, gas_limit, network)


@asset_cmd.command('balanceOf')
@click.option('--asset', nargs=1, type=str, default='', help='Asset of ONT or ONG (default: "ont")')
@click.option('--address', nargs=1, type=str, default='', help='query balance of the address')
@click.option('--network', nargs=1, type=str, default='', help='which network will be used,default test network')
@click.pass_context
def balance_of(ctx, asset, address, network):
    """
    query balance of the address.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Asset.balance_of(project_dir, asset, address, network)


@asset_cmd.command('withdrawOng')
@click.option('--claimer', nargs=1, type=str, default='', help='Transfer-out account <address>')
@click.option('--to', nargs=1, type=str, default='', help='Transfer-in account <address>')
@click.option('--amount', nargs=1, type=int, default=0, help='Transfer <amount>.int number')
@click.option('--gas_price', nargs=1, type=int, default=500, help='Gas price of transaction (default: 500)')
@click.option('--gas_limit', nargs=1, type=int, default=20000, help='Gas limit of the transaction (default: 20000)')
@click.option('--network', nargs=1, type=str, default='', help='which network will be used,default test network')
@click.pass_context
def withdraw_ong(ctx, claimer, to, amount, gas_price, gas_limit, network):
    """
    withdraw unbound ong.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Asset.withdraw_ong(project_dir, claimer, to, amount, gas_limit, gas_price, network)


@asset_cmd.command('unboundOng')
@click.option('--address', nargs=1, type=str, default='', help='query unbound ong of the address')
@click.option('--network', nargs=1, type=str, default='', help='which network will be used,default test network')
@click.pass_context
def query_unbound_ong(ctx, address, network):
    """
    query unbound ong.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Asset.query_unbound_ong(project_dir, address, network)