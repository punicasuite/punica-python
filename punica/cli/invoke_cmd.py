#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from ontology.exception.exception import SDKException

from .main import main

from punica.invoke.invoke_contract import Invoke
from punica.exception.punica_exception import PunicaException


@main.command('invoke')
@click.option('--network', nargs=1, type=str, default='', help='Specify which network the contracts will be deployed.')
@click.option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@click.option('--functions', nargs=1, type=str, default='', help='Specify which function will be executed.')
@click.option('--config', nargs=1, type=str, default='', help='Specify which config file will be used.')
@click.option('--list', nargs=0, help='list all functions.')
@click.pass_context
def invoke_cmd(ctx, network, wallet, functions, config, list):
    """
    Invoke the function list in punica-config.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        Invoke.invoke_all_function_in_list(list, wallet, project_dir, network, functions, config)
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        print('Punica will exist...')
        exit(1)
