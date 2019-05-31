#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import binascii
import os

import urllib3
import requests

from boa.compiler import Compiler

from punica.exception.punica_exception import PunicaException, PunicaError
from punica.utils.file_system import ensure_file_exists

V1_PY_CONTRACT_COMPILE_URL = "https://smartxcompiler.ont.io/api/v1.0/python/compile"
V2_PY_CONTRACT_COMPILE_URL = "https://smartxcompiler.ont.io/api/v2.0/python/compile"
CSHARP_CONTRACT_COMPILE_URL = "https://smartxcompiler.ont.io/api/v1.0/csharp/compile"


class PunicaCompiler:
    @staticmethod
    def __to_hex_avm(raw_avm: str):
        hex_avm = binascii.hexlify(raw_avm).decode('ascii')
        return hex_avm

    @staticmethod
    def __raw_avm_file_to_hex_code(avm_path: str):
        with open(avm_path, 'rb') as f:
            raw_avm = f.read().decode()
            hex_avm = PunicaCompiler.__to_hex_avm(raw_avm)
            return hex_avm

    @staticmethod
    def generate_avm_code(contract_path: str):
        compiler = Compiler.load(contract_path)
        raw_avm = compiler.write()
        hex_avm = PunicaCompiler.__to_hex_avm(raw_avm)
        return hex_avm

    @staticmethod
    def generate_avm_file(contract_path: str, save_path: str = ''):
        if save_path == '':
            split_path = os.path.split(contract_path)
            save_path = os.path.join(os.path.dirname(split_path[0]), 'build', split_path[1])
            save_path = save_path.replace('.py', '.avm')
        hex_avm = PunicaCompiler.generate_avm_code(contract_path)
        split_path = os.path.split(save_path)
        if not os.path.exists(split_path[0]):
            os.makedirs(split_path[0])
        with open(save_path, 'w') as f:
            f.write(hex_avm)

    @staticmethod
    def compile_contract(contract_path: str, local: bool = False, save_path: str = ''):
        if save_path == '':
            split_path = os.path.split(contract_path)
            save_path = os.path.join(os.path.dirname(split_path[0]), 'build', split_path[1])
            if save_path.endswith('.py'):
                save_path = save_path.replace('.py', '.avm')
            else:
                save_path = save_path.replace('.cs', '.avm')
        if not local:
            PunicaCompiler.compile_in_remote(contract_path)
            return
        try:
            PunicaCompiler.generate_avm_file(contract_path, save_path)
            print('Compiled, enjoy your contract.')
        except PermissionError as error:
            if error.args[0] == 13:
                raise PunicaException(PunicaError.permission_error)
            else:
                raise PunicaException(PunicaError.other_error(error.args[1]))

    @staticmethod
    def generate_compile_payload(contract_path: str):
        payload = dict()
        with open(contract_path, "r") as f:
            payload['code'] = f.read()
        payload['type'] = PunicaCompiler.get_contract_type(contract_path)
        return payload

    @staticmethod
    def is_v2_py_contract(contract_code: str):
        return True if "OntCversion = '2.0.0'" in contract_code[:30] else False

    @staticmethod
    def get_contract_type(contract_path: str) -> str:
        return 'Python' if contract_path.endswith('.py') else 'CSharp'

    @staticmethod
    def get_compiler_url(contract_path: str, is_neo_boa: bool = False):
        if contract_path.endswith('.py'):
            if is_neo_boa:
                return V1_PY_CONTRACT_COMPILE_URL
            else:
                return V2_PY_CONTRACT_COMPILE_URL
        return CSHARP_CONTRACT_COMPILE_URL

    @staticmethod
    def save_avm_file(avm: str, path: str):
        ensure_file_exists(path)
        with open(path, "w", encoding='utf-8') as f:
            f.write(avm.lstrip('b\'').rstrip('\''))

    @staticmethod
    def save_abi_file(abi: str, path: str):
        with open(path, "w", encoding='utf-8') as f:
            json.dump(json.loads(abi), f, indent=2)

    @staticmethod
    def compile_in_remote(contract_path: str, is_neo_boa: bool = False):
        header = {'Content-type': 'application/json'}
        payload = PunicaCompiler.generate_compile_payload(contract_path)
        url = PunicaCompiler.get_compiler_url(contract_path, is_neo_boa)
        path = os.path.dirname(contract_path)
        file_name = os.path.basename(contract_path).split(".")
        urllib3.disable_warnings()
        res = requests.post(url, json=payload, headers=header, timeout=10, verify=False)
        result = json.loads(res.content)
        if result["errcode"] != 0:
            print("compile failed")
            print(result)
        avm_save_path = os.path.join(path, 'build', ''.join([file_name[0], '.avm']))
        PunicaCompiler.save_avm_file(result.get('avm', ''), avm_save_path)
        abi_save_path = os.path.join(path, 'build', ''.join([file_name[0], "_abi.json"]))
        PunicaCompiler.save_abi_file(result.get('abi', ''), abi_save_path)
        print("Compiled, Thank you")
