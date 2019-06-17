#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from click import argument

from ontology.exception.exception import SDKException

from .main import main

from punica.deploy.deploy_contract import Deploy
from punica.exception.punica_exception import PunicaException


@main.command('deploy')
@argument('contract', default='')
@click.option('--network', nargs=1, type=str, default='', help='Specify which network the contracts will be deployed.')
@click.option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@click.option('--config', nargs=1, type=str, default='', help='Specify which deploy config file will be used.')
@click.pass_context
def deploy_cmd(ctx, contract, network, wallet, config):
    """
    Deploy contracts to specified network.
    """
    project_dir = ctx.obj['PROJECT_DIR']

    try:
        tx_hash = Deploy.deploy_smart_contract(project_dir, network, contract, wallet, config)
        if tx_hash is not None:
            hex_contract_address = Deploy.generate_contract_address(project_dir, contract)
            print('\tDeploy to: {}'.format(hex_contract_address))
            if Deploy.check_deploy_state(tx_hash, project_dir, network):
                print('Deploy successful to network...')
                print('\t Contract address is {}'.format(hex_contract_address))
                print('\t Txhash is {}'.format(tx_hash))
            else:
                print('Deploy unsuccessfully...')
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        exit(1)
