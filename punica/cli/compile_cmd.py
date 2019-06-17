#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os import path

from halo import Halo
from click import echo, pass_context, option
from ontology.exception.exception import SDKException

from .main import main
from punica.compile.py_contract import compile_contract, search_contract
from punica.exception.punica_exception import PunicaException


@main.command('compile')
@option('--contract', nargs=1, type=str, default='', help='Compile specified contract file in contracts dir.')
@pass_context
def compile_cmd(ctx, contract):
    """
    Compile contract source files
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        spinner = Halo(text='Compiling...', spinner='dots')
        spinner.start()
        if len(contract) == 0:
            contract_path_list = search_contract(project_dir)
            for contract_path in contract_path_list:
                compile_contract(contract_path)
        else:
            contract_path = path.join(project_dir, 'contracts', contract)
            compile_contract(contract_path)
    except (PunicaException, SDKException) as e:
        echo('An error occur...')
        echo(e.args[1])
