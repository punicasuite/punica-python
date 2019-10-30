from click import argument, option, echo, pass_context

from ontology.exception.exception import SDKException

from .main import main
from punica.utils.output import echo_cli_exception
from punica.deploy.deploy_contract import Deployment
from punica.exception.punica_exception import PunicaException


@main.command('deploy')
@argument('contract_name', default='')
@option('--network', nargs=1, type=str, default='', help='Specify which network the build will be deployed.')
@option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@option('--config', nargs=1, type=str, default='', help='Specify which deploy config file will be used.')
@option('--wasm', is_flag=True, help='Deploy WebAssembly contract into network.')
@pass_context
def deploy_cmd(ctx, contract_name, network, wallet, config, wasm):
    """
    Deploy contract to specified network.
    """
    echo('\nDeploying your contract...')
    echo('===========================\n')
    try:
        deployment = Deployment(ctx.obj['PROJECT_DIR'], network, wallet, config)
        if len(contract_name) == 0:
            if wasm:
                wasm_file_list = deployment.get_all_wasm_file()
                for file in wasm_file_list:
                    deployment.deploy_wasm_contract(file)
            else:
                avm_file_list = deployment.get_all_avm_file()
                for file in avm_file_list:
                    deployment.deploy_neo_contract(file)
        else:
            if wasm:
                deployment.deploy_wasm_contract(contract_name)
            else:
                deployment.deploy_neo_contract(contract_name)
    except (PunicaException, SDKException) as e:
        echo_cli_exception(e)
