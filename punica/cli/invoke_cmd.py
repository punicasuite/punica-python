from click import (
    option,
    pass_context
)

from ontology.exception.exception import SDKException

from .main import main
from punica.invoke.invoke_contract import Invoke
from punica.utils.output import echo_cli_exception
from punica.exception.punica_exception import PunicaException


@main.group('invoke', invoke_without_command=True)
@option('--network', nargs=1, type=str, default='', help='Specify which network the contracts will be deployed.')
@option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@option('--functions', nargs=1, type=str, default='', help='Specify which function will be executed.')
@option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@option('--preexec', nargs=1, type=str, default='', help='PreExec the function.')
@pass_context
def invoke_cmd(ctx, network, wallet, functions, config, preexec):
    """
    Invoke the function list in default-config or specify config.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    if ctx.invoked_subcommand is None:
        try:
            Invoke.invoke_all_function_in_list(wallet, project_dir, network, functions, config, preexec)
        except (PunicaException, SDKException) as e:
            echo_cli_exception(e)
    else:
        pass


@invoke_cmd.command('list')
@option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@pass_context
def list_cmd(ctx, config):
    """
    List all the function in default-config or specify config.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Invoke.list_all_functions(project_dir, config)
