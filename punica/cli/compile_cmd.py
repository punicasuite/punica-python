#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os import path

from halo import Halo
from click import echo, pass_context, option, argument
from ontology.exception.exception import SDKException

from .main import main
from punica.compile.py_contract import PyContract
from punica.exception.punica_exception import PunicaException


@main.command('compile')
@argument('contract', default='')
@pass_context
def compile_cmd(ctx, contract_name: str):
    """
    Compile contract source files
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        spinner = Halo(text='Compiling...', spinner='dots')
        spinner.start()
        py_contract = PyContract(project_dir)
        if len(contract_name) == 0:
            contract_name_list = py_contract.get_all_contract()
            for contract_name in contract_name_list:
                py_contract.compile_contract(contract_name)
            return
        if not contract_name.endswith('.py'):
            contract_name += '.py'
        py_contract.compile_contract(contract_name)
    except (PunicaException, SDKException) as e:
        echo('An error occur...')
        echo(e.args[1])
