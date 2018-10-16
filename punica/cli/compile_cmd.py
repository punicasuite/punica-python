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
    print('\tEnjoy your contracts:)')


@main.command('compile')
@click.option('--contracts', nargs=1, type=str, default='', help='Compile specified contracts files in contracts dir.')
# @click.option('--avm', nargs=1, type=str, default=False, help='Only generate avm file flag.')
# @click.option('--abi', nargs=1, type=str, default=False, help='Only generate abi file flag.')
@click.option('--local', nargs=1, type=str, default=False, help='Use local compiler.')
@click.pass_context
def compile_cmd(ctx, contracts, local):
    """
    Compile the specified contracts to avm and abi file.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        print('Compile...')
        contract_dir = os.path.join(project_dir, 'contracts')
        if contracts != '':
            contract_dir2 = os.path.join(contract_dir, contracts)
            if os.path.isfile(contract_dir2) and contracts.endswith('.py'):
                compile_contract(contract_dir, contracts, False, False, local)
        else:
            contract_name_list = os.listdir(contract_dir)
            for contract_name in contract_name_list:
                if contract_name.startswith('__') or contract_name.endswith('.json') or contract_name == 'build':
                    continue
                contract_dir2 = os.path.join(contract_dir, contract_name)
                if os.path.isdir(contract_dir2):
                    contract_name_list2 = os.listdir(contract_dir2)
                    for contract_name2 in contract_name_list2:
                        if contract_name2.startswith('__') or contract_name.endswith('.json'):
                            continue
                        contract_dir3 = os.path.join(contract_dir2, contract_name2)
                        if os.path.isdir(contract_dir3):
                            raise RuntimeError("Nested too deep")
                        elif os.path.isfile(contract_dir3) and contract_name2.endswith('.py'):
                            compile_contract(contract_dir2, contract_name2, False, False, local)
                        else:
                            raise RuntimeError("only support py contract")
                elif os.path.isfile(contract_dir2) and contract_name.endswith('.py'):
                    compile_contract(contract_dir, contract_name, False, False, local)
                else:
                    raise RuntimeError("contract path is wrong")
        print('Now we are finished :)')
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        exit(1)
