#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from ontology.exception.exception import SDKException

from .main import main

from punica.deploy.deploy_contract import Deploy
from punica.exception.punica_exception import PunicaException


@main.command('deploy')
@click.option('--network', nargs=1, type=str, default='', help='Specify which network the contracts will be deployed.')
@click.option('--avm', nargs=1, type=str, default='', help='Specify which avm file will be deployed.')
@click.option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@click.option('--config', nargs=1, type=str, default='', help='Specify which deploy config file will be used.')
@click.pass_context
def deploy_cmd(ctx, network, avm, wallet, config):
    """
    Deploys the specified contracts to specified chain.
    """
    project_dir = ctx.obj['PROJECT_DIR']

    try:
        tx_hash = Deploy.deploy_smart_contract(project_dir, network, avm, wallet, config)
        if tx_hash is not None:
            hex_contract_address = Deploy.generate_contract_address(project_dir, avm)
            print('\tDeploy to: 0x{}'.format(hex_contract_address))
            if Deploy.check_deploy_state(tx_hash, project_dir, network):
                print('Deploy successful to network...')
                print('\t... 0x{}'.format(tx_hash))
            else:
                print('Deploy unsuccessfully...')
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        print('Punica will exist...')
        exit(1)
