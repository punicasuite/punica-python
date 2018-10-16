import click

from punica.account.account import Account
from .main import main


@main.command('account')
@click.option('--add', nargs=0, help='Compile specified contracts files in contracts dir.')
@click.option('--l', nargs=0, help='Only generate avm file flag.')
@click.option('--delete', nargs=1, type=str, default='', help='Only generate abi file flag.')
@click.option('--i', nargs=1, type=str, default='', help='Use local compiler.')
@click.pass_context
def account_cmd(ctx, add, l, delete, i):
    """
    Account information.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Account.execute(project_dir, add, l, delete, i)

