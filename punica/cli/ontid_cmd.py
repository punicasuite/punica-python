import click

from punica.ontid.ontid import OntId
from .main import main


@main.group('ontid', invoke_without_command=True)
@click.pass_context
def ontid_cmd(ctx):
    """
    manager your ont_id, list or add.
    """
    pass


@ontid_cmd.command('add')
@click.pass_context
def add_amd(ctx):
    """
    add ont_id.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    OntId.add_ont_id(project_dir)


@ontid_cmd.command('list')
@click.pass_context
def list_amd(ctx):
    """
    list all the ont_id in wallet.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    OntId.list_ont_id(project_dir)


