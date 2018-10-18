

import click

from punica.wallet.account import Account
from punica.wallet.asset import Asset
from punica.wallet.ontid import OntId

from .main import main, CONTEXT_SETTINGS


@main.group('wallet', invoke_without_command=True)
@click.pass_context
def wallet_cmd(ctx):
    """
    Manager your asset, ontid, account.
    """
    if ctx.invoked_subcommand is None:
        print('Usage: punica wallet [OPTIONS] COMMAND [ARGS]...')
        print('')
        print('  ', 'Manager your asset, ontid, account.')
        print()
        print('Options:')
        print('  ', '-h, --help  Show this message and exit.')
        print()
        print('Commands:')
        print('  ', 'account  Manager your account.')
        print('  ', 'asset    Manager your asset, transfer, balance,...')
        print('  ', 'ontid    Manager your ont_id, list or add.')
    else:
        pass


@wallet_cmd.group('ontid', invoke_without_command=True)
@click.pass_context
def ontid_cmd(ctx):
    """
    Manager your ont_id, list or add.
    """
    if ctx.invoked_subcommand is None:
        print('Usage: punica wallet [OPTIONS] COMMAND [ARGS]...')
        print('')
        print('  ', 'Manager your asset, ontid, account.')
        print()
        print('Options:')
        print('  ', '-h, --help  Show this message and exit.')
        print()
        print('Commands:')
        print('  ', 'add   Add ont_id to wallet.')
        print('  ', 'list  List all the ont_id in wallet.')
    else:
        pass


@ontid_cmd.command('add')
@click.pass_context
def add_amd(ctx):
    """
    Add ont_id to wallet.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    OntId.add_ont_id(project_dir)


@ontid_cmd.command('list')
@click.pass_context
def list_amd(ctx):
    """
    List all the ont_id in wallet.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    OntId.list_ont_id(project_dir)


@wallet_cmd.group('account', invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def account_cmd(ctx):
    """
    Manager your account.
    """
    if ctx.invoked_subcommand is None:
        print('Usage: punica wallet account [OPTIONS] COMMAND [ARGS]...')
        print('')
        print('  ', 'Manager your account.')
        print()
        print('Options:')
        print('  ', '-h, --help  Show this message and exit.')
        print()
        print('Commands:')
        print('  ', 'add     Add account to wallet.json.')
        print('  ', 'delete  Delete account by address.')
        print('  ', 'import  Import account by private key.')
        print('  ', 'list    List all your account address.')
    else:
        pass


@account_cmd.command('import')
@click.option('--privatekey', nargs=1, type=str, default='', help='import account by privatekey.')
@click.pass_context
def import_cmd(ctx, privatekey):
    """
    delete account by address.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Account.import_account(project_dir, privatekey)


@account_cmd.command('delete')
@click.option('--address', nargs=1, type=str, default='', help='Delete account by address.')
@click.pass_context
def delete_cmd(ctx, address):
    """
    delete account by address.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Account.delete_account(project_dir, address)


@account_cmd.command('list')
@click.pass_context
def list_cmd(ctx):
    """
    List all your account address.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Account.list_account(project_dir)


@account_cmd.command('add')
@click.pass_context
def add_cmd(ctx):
    """
    Add account to wallet.json.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Account.add_account(project_dir)
    print('create account successful')


@wallet_cmd.group('asset', invoke_without_command=True)
@click.pass_context
def asset_cmd(ctx):
    """
    Manager your asset, transfer, balance, withdraw ong, unbound ong.
    """
    if ctx.invoked_subcommand is None:
        print('Usage: punica wallet asset [OPTIONS] COMMAND [ARGS]...')
        print('')
        print('  ', 'Manager your asset, transfer, balance, withdraw ong, unbound ong.')
        print()
        print('Options:')
        print('  ', '-h, --help  Show this message and exit.')
        print()
        print('Commands:')
        print('  ', 'balanceOf    Query balance of the address.')
        print('  ', 'transfer     Transfer your asset to another address.')
        print('  ', 'unboundOng   Query unbound ong.')
        print('  ', 'withdrawOng  Withdraw unbound ong.')
    else:
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
    Transfer your asset to another address.
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
    Query balance of the address.
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
    Withdraw unbound ong.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Asset.withdraw_ong(project_dir, claimer, to, amount, gas_limit, gas_price, network)


@asset_cmd.command('unboundOng')
@click.option('--address', nargs=1, type=str, default='', help='query unbound ong of the address')
@click.option('--network', nargs=1, type=str, default='', help='which network will be used,default test network')
@click.pass_context
def query_unbound_ong(ctx, address, network):
    """
    Query unbound ong.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Asset.query_unbound_ong(project_dir, address, network)