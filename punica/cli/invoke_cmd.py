from click import (
    echo,
    option,
    pass_context,
    argument
)

from ontology.exception.exception import SDKException

from .main import main
from punica.invoke.invoke_contract import Invocation
from punica.utils.output import echo_cli_exception
from punica.exception.punica_exception import PunicaException


@main.group('invoke', invoke_without_command=True)
@argument('func_name', default='')
@option('--network', nargs=1, type=str, default='', help='Specify which network the contracts will be deployed.')
@option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@pass_context
def invoke_cmd(ctx, func_name, network, wallet, config):
    """
    Invoke the contract methods in contract config file.
    """
    echo('\nInvoking your contracts...')
    echo('==========================\n')
    try:
        invocation = Invocation(ctx.obj['PROJECT_DIR'], network, wallet, config)
        punica_func_list = invocation.get_func_list()
        if len(func_name) == 0:
            for func in punica_func_list:
                invocation.invoke(func)
        else:
            func = invocation.get_func_by_name(func_name)
            invocation.invoke(func)
    except (PunicaException, SDKException) as e:
        echo_cli_exception(e)

# @invoke_cmd.command('list')
# @option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
# @pass_context
# def list_cmd(ctx, config):
#     """
#     List all the function in default-config or specify config.
#     """
#     project_dir = ctx.obj['PROJECT_DIR']
#     Invocation.list_all_functions(project_dir, config)
