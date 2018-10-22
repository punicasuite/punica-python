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
    print('Compile', contract_name)
    if avm:
        PunicaCompiler.generate_avm_file(contract_path)
        print('\tGenerate avm file successful...')
    if abi:
        PunicaCompiler.generate_abi_file(contract_path)
        print('\tGenerate abi file successful...')
    if not avm and not abi:
        PunicaCompiler.compile_contract(contract_path, local)


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
        print('Compile')
        if contracts != '':
            contract_file_path = os.path.join(project_dir, contracts)
            if not os.path.exists(contract_file_path):
                contract_file_path = os.path.join(project_dir, 'contracts', contracts)
            if contracts.endswith('.py') or contracts.endswith('.cs'):
                compile_contract(os.path.dirname(contract_file_path), os.path.basename(contract_file_path), False, False, local)
            else:
                print('Compile Error')
                print('file type is wrong')
                os._exit(0)
        else:
            contract_dir = os.path.join(project_dir, 'contracts')
            contract_name_list = os.listdir(contract_dir)
            for contract_name in contract_name_list:
                if contract_name.startswith('__') or contract_name.endswith('.json') or contract_name == 'build':
                    continue
                contract_file_path = os.path.join(contract_dir, contract_name)
                if os.path.isdir(contract_file_path):
                    contract_name_list_sub = os.listdir(contract_file_path)
                    for contract_name_sub in contract_name_list_sub:
                        if contract_name_sub.startswith('__') or contract_name.endswith('.json'):
                            continue
                        contract_file_path_sub = os.path.join(contract_file_path, contract_name_sub)
                        if os.path.isdir(contract_file_path_sub):
                            raise RuntimeError("Nested too deep")
                        elif os.path.isfile(contract_file_path_sub):
                            if contract_file_path_sub.endswith('.py') or contract_file_path_sub.endswith('.cs'):
                                compile_contract(os.path.dirname(contract_file_path_sub),
                                                 os.path.basename(contract_file_path_sub), False, False, local)
                            else:
                                print('Compile Error')
                                print('file type is wrong')
                                os._exit(0)
                elif os.path.isfile(contract_file_path):
                    if contract_name.endswith('.py') or contract_name.endswith('.cs'):
                        compile_contract(os.path.dirname(contract_file_path), os.path.basename(contract_file_path),
                                         False, False, local)
                    else:
                        print('Compile Error')
                        print('file type is wrong')
                        os._exit(0)
                else:
                    raise RuntimeError("contract path is wrong")
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        exit(1)
