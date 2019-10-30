import time

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


@main.command('invoke')
@argument('func_name', default='')
@option('--network', nargs=1, type=str, default='', help='Specify which network the build will be deployed.')
@option('--wallet', '-w', 'wallet_path', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@option('--sleep', nargs=1, type=int, default=0, help='Time to sleep between each invocation.')
@option('--pre', is_flag=True, help='Prepare execute transaction, without commit to ledger.')
@pass_context
def invoke_cmd(ctx, func_name, network, wallet_path, config, sleep, pre):
    """
    Invoke the contract methods in contract config file.
    """
    echo('\nInvoking your build...')
    echo('==========================\n')
    try:
        invocation = Invocation(ctx.obj['PROJECT_DIR'], network, wallet_path, config)
        punica_func_list = invocation.get_func_list()
        if len(func_name) == 0:
            for func in punica_func_list:
                invocation.invoke(func, pre)
                time.sleep(sleep)
        else:
            func = invocation.get_func_by_name(func_name)
            invocation.invoke(func, pre)
    except (PunicaException, SDKException) as e:
        echo_cli_exception(e)
