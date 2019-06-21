from click import (
    option,
    pass_context,
    argument)

from ontology.exception.exception import SDKException

from .main import main
from punica.invoke.invoke_contract import Invocation
from punica.utils.output import echo_cli_exception
from punica.exception.punica_exception import PunicaException


@main.group('invoke', invoke_without_command=True)
@argument('func', default='')
@option('--network', nargs=1, type=str, default='', help='Specify which network the contracts will be deployed.')
@option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@pass_context
def invoke_cmd(ctx, func, network, wallet, config):
    """
    Invoke the contract in default-config or specify config.
    """
    try:
        invocation = Invocation(ctx.obj['PROJECT_DIR'], network, wallet, config)
        func_list = invocation.get_func_list()
        if len(func) == 0:
            for func in func_list:
                invocation.invoke(func)

        Invocation.invoke_all_function_in_list(wallet, project_dir, network, functions, config, preexec)
    except (PunicaException, SDKException) as e:
        echo_cli_exception(e)


@invoke_cmd.command('list')
@option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@pass_context
def list_cmd(ctx, config):
    """
    List all the function in default-config or specify config.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Invocation.list_all_functions(project_dir, config)
