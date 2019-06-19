import click
from click import argument

from ontology.exception.exception import SDKException

from .main import main
from punica.utils.output import echo_cli_exception
from punica.deploy.deploy_contract import Deployment
from punica.exception.punica_exception import PunicaException


@main.command('deploy')
@argument('contract_name', default='')
@click.option('--network', nargs=1, type=str, default='', help='Specify which network the contracts will be deployed.')
@click.option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@click.option('--config', nargs=1, type=str, default='', help='Specify which deploy config file will be used.')
@click.pass_context
def deploy_cmd(ctx, contract_name, network, wallet, config):
    """
    Deploy contracts to specified network.
    """
    deployment = Deployment(ctx.obj['PROJECT_DIR'], network, wallet, config)
    try:
        if len(contract_name) == 0:
            avm_file_list = deployment.get_all_avm_file()
            for file in avm_file_list:
                deployment.deploy_smart_contract(file)
        else:
            deployment.deploy_smart_contract(contract_name)
    except (PunicaException, SDKException) as e:
        echo_cli_exception(e)
