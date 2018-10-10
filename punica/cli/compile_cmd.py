#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import click

from .main import main

from punica.compile.contract_compile import PunicaCompiler


def compile_contract(contract_dir, contract_name, avm, abi):
    contract_path = os.path.join(contract_dir, contract_name)
    print('\tCompile {}...'.format(contract_name))
    if avm:
        PunicaCompiler.generate_avm_file(contract_path)
        print('\tGenerate avm file successful...')
    if abi:
        PunicaCompiler.generate_abi_file(contract_path)
        print('\tGenerate abi file successful...')
    if not avm and not abi:
        PunicaCompiler.compile_contract(contract_path)
        print('\tGenerate abi file and avm file successful...')
    print('\tEnjoy your contract:)')


@main.command('compile')
@click.option('--contract', nargs=1, type=str, default='', help='Compile all contract files in contracts dir.')
@click.option('--avm', nargs=1, type=str, default=False, help='Only generate avm file flag.')
@click.option('--abi', nargs=1, type=str, default=False, help='Only generate abi file flag.')
@click.pass_context
def compile_cmd(ctx, contract, avm, abi):
    """
    Compile the specified contracts to avm and abi file.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    contract_dir = os.path.join(project_dir, 'contracts')
    print('Compile...')
    if contract != '':
        compile_contract(contract_dir, contract, avm, abi)
    else:
        contract_list = os.listdir(contract_dir)
        for contract in contract_list:
            compile_contract(contract_dir, contract, avm, abi)
    print('Now we are finished :)')
