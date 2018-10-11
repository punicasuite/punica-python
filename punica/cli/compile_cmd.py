#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import click
from ontology.exception.exception import SDKException

from .main import main

from punica.compile.contract_compile import PunicaCompiler
from punica.exception.punica_exception import PunicaException


def compile_contract(contract_dir, contract_name, avm, abi, local):
    contract_path = os.path.join(contract_dir, contract_name)
    print('\tCompile {}...'.format(contract_name))
    if avm:
        PunicaCompiler.generate_avm_file(contract_path)
        print('\tGenerate avm file successful...')
    if abi:
        PunicaCompiler.generate_abi_file(contract_path)
        print('\tGenerate abi file successful...')
    if not avm and not abi:
        PunicaCompiler.compile_contract(contract_path, local)
        print('\tGenerate abi file and avm file successful...')
    print('\tEnjoy your contract:)')


@main.command('compile')
@click.option('--contract', nargs=1, type=str, default='', help='Compile all contract files in contracts dir.')
@click.option('--avm', nargs=1, type=str, default=False, help='Only generate avm file flag.')
@click.option('--abi', nargs=1, type=str, default=False, help='Only generate abi file flag.')
@click.option('--local', nargs=1, type=str, default=False, help='Use local compiler.')
@click.pass_context
def compile_cmd(ctx, contract, avm, abi, local):
    """
    Compile the specified contracts to avm and abi file.
    """
    project_dir = ctx.obj['PROJECT_DIR']

    try:
        contract_dir = os.path.join(project_dir, 'contracts')
        print('Compile...')
        if contract != '':
            compile_contract(contract_dir, contract, avm, abi, local)
        else:
            contract_list = os.listdir(contract_dir)
            for contract in contract_list:
                compile_contract(contract_dir, contract, avm, abi, local)
        print('Now we are finished :)')
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print('Punica will exist...')
        exit(1)
