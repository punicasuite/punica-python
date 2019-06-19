from ontology.exception.exception import SDKException

from click import (
    argument,
    pass_context,
    echo
)

from .main import main
from punica.compile.py_contract import PyContract
from punica.utils.output import echo_cli_exception
from punica.exception.punica_exception import PunicaException


@main.command('compile')
@argument('contract_name', default='')
@pass_context
def compile_cmd(ctx, contract_name: str):
    """
    Compile contract source files
    """
    py_contract = PyContract(ctx.obj['PROJECT_DIR'])
    echo('\nCompiling your contracts...')
    echo('===========================\n')
    try:
        if len(contract_name) == 0:
            contract_name_list = py_contract.get_all_contract()
            for contract_name in contract_name_list:
                py_contract.compile_contract(contract_name)
            return
        if not contract_name.endswith('.py'):
            contract_name += '.py'
        py_contract.compile_contract(contract_name)
    except (PunicaException, SDKException) as e:
        echo_cli_exception(e)
