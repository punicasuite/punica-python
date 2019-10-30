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
@option('--wasm', is_flag=True, help='Invoke WebAssembly contract.')
@pass_context
def invoke_cmd(ctx, func_name, network, wallet_path, config, sleep, pre, wasm):
    """
    Invoke the contract methods in contract config file.
    """
    try:
        invocation = Invocation(ctx.obj['PROJECT_DIR'], network, wallet_path, config, wasm)
        invocation.echo_invoke_banner()
        if len(func_name) == 0:
            punica_func_list = invocation.get_func_list()
            for func in punica_func_list:
                if invocation.is_wasm:
                    invocation.invoke_wasm_contract(func, pre)
                else:
                    invocation.invoke_neo_contract(func, pre)
            time.sleep(sleep)
        else:
            func = invocation.get_func_by_name(func_name)
            if invocation.is_wasm:
                invocation.invoke_wasm_contract(func, pre)
            else:
                invocation.invoke_neo_contract(func, pre)
    except (PunicaException, SDKException) as e:
        echo_cli_exception(e)
