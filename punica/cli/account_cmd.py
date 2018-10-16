import click

from punica.account.account import Account
from .main import main


@main.group('account', invoke_without_command=True)
@click.option('--delete', nargs=1, type=str, default='', help='Delete account by address.')
@click.option('--i', nargs=1, type=str, default='', help='Import account by private key')
@click.pass_context
def account_cmd(ctx, delete, i):
    """
    Account information.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Account.execute(project_dir, delete, i)


@account_cmd.command('list')
@click.pass_context
def list_cmd(ctx):
    project_dir = ctx.obj['PROJECT_DIR']
    Account.list_account(project_dir)


@account_cmd.command('add')
@click.pass_context
def add_cmd(ctx):
    project_dir = ctx.obj['PROJECT_DIR']
    Account.add_account(project_dir)
    print('create account successful')


