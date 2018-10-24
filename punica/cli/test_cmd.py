#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from ontology.exception.exception import SDKException

from punica.test.test import Test
from .main import main

from punica.exception.punica_exception import PunicaException


@main.group('test', invoke_without_command=True)
@click.option('--file', nargs=1, type=str, default='', help='Specify which test file will be used.')
@click.pass_context
def test_cmd(ctx, file):
    """
    Unit test with specified smart contract
    """
    if ctx.invoked_subcommand is None:
        project_dir = ctx.obj['PROJECT_DIR']
        Test.test_file(project_dir, file)
    else:
        pass


@test_cmd.command('template')
@click.option('--abi', nargs=1, type=str, default='', help='Specify which abi file will be used.')
@click.pass_context
def template_cmd(ctx, abi):
    """
    generate test template file
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        Test.generate_test_template(project_dir, '', abi)
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        print('Punica will exist...')
        exit(1)