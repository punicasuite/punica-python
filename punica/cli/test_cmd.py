#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from ontology.exception.exception import SDKException

from punica.test.test import Test
from .main import main

from punica.exception.punica_exception import PunicaException


@main.command('test')
@click.option('--config', nargs=1, type=str, default='', help='Specify which config file will be used. '
                                                              'default is default-config.json')
@click.option('--abi', nargs=1, type=str, default='', help='Specify which abi file will be used.')
@click.pass_context
def test_cmd(ctx, config, abi):
    """
    generate test template file
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        Test.generate_test_template(project_dir, config, abi)
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        print('Punica will exist...')
        exit(1)
