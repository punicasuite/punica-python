import click

from punica.list.list_punica import ListPunica
from .main import main


@main.command('list')
@click.option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@click.pass_context
def list_cmd(ctx, config):
    project_dir = ctx.obj['PROJECT_DIR']
    ListPunica.list_funcs(project_dir, config)