#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from os import path
from typing import List

import urllib3
import requests

from halo import Halo
from click import echo

from punica.exception.punica_exception import PunicaException, PunicaError
from punica.utils.file_system import ensure_file_exists

V1_PY_CONTRACT_COMPILE_URL = "https://smartxcompiler.ont.io/api/v1.0/python/compile"
V2_PY_CONTRACT_COMPILE_URL = "https://smartxcompiler.ont.io/api/v2.0/python/compile"
CSHARP_CONTRACT_COMPILE_URL = "https://smartxcompiler.ont.io/api/v1.0/csharp/compile"


def search_contract(project_dir: str) -> List[str]:
    contract_dir = os.path.join(project_dir, 'contracts')
    files_in_dir = os.listdir(contract_dir)
    contract_path_list = list()
    for file in files_in_dir:
        if not file.endswith('.py'):
            continue
        contract_path_list.append(os.path.join(contract_dir, file))
    return contract_path_list


def compile_contract(contract_path: str, save_path: str = ''):
    prepare_spinner = Halo(text="Preparing to compile", spinner='dots')
    prepare_spinner.start()
    if len(save_path) == 0:
        split_path = os.path.split(contract_path)
        save_path = os.path.join(os.path.dirname(split_path[0]), 'build', split_path[1])
        if save_path.endswith('.py'):
            save_path = save_path.replace('.py', '.avm')
        else:
            prepare_spinner.fail()
            echo('Punica is currently supporting contract in Python.')
            return False
    ensure_file_exists(save_path)
    prepare_spinner.succeed()
    compile_spinner = Halo(text="Compiling your contracts...", spinner='bouncingBar')
    compile_spinner.start()
    compile_py_contract_in_remote(contract_path, save_path)
    compile_spinner.succeed()
    return True


def compile_py_contract_in_remote(contract_path: str, save_path: str):
    payload = generate_compile_payload(contract_path)
    url = get_compiler_url(contract_path)
    urllib3.disable_warnings()
    res = requests.post(url, json=payload, headers={'Content-type': 'application/json'}, timeout=10, verify=False)
    result = json.loads(res.content)
    if result["errcode"] != 0:
        echo("An error occur in remote server.")
        return False
    save_avm_file(result.get('avm', ''), save_path)
    return True


def save_avm_file(avm_code: str, to_path: str):
    try:
        with open(to_path, 'w') as f:
            f.write(normalize_avm_code(avm_code))
    except PermissionError as error:
        if error.args[0] == 13:
            raise PunicaException(PunicaError.permission_error)
        else:
            raise PunicaException(PunicaError.other_error(error.args[1]))


def normalize_avm_code(avm_code: str):
    return avm_code.lstrip('b\'').rstrip('\'')


def generate_compile_payload(contract_path: str):
    payload = dict()
    with open(contract_path, "r") as f:
        payload['code'] = f.read()
    payload['type'] = get_contract_type(contract_path)
    return payload


def is_v2_py_contract(contract_code: str):
    return True if "OntCversion = '2.0.0'" in contract_code[:30] else False


def get_contract_type(contract_path: str) -> str:
    return 'Python' if contract_path.endswith('.py') else 'CSharp'


def get_compiler_url(contract_path: str, is_neo_boa: bool = False):
    if contract_path.endswith('.py'):
        if is_neo_boa:
            return V1_PY_CONTRACT_COMPILE_URL
        else:
            return V2_PY_CONTRACT_COMPILE_URL
    return CSHARP_CONTRACT_COMPILE_URL
