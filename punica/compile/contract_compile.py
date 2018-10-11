#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import binascii
import os

import requests
from boa.util import Digest
from boa.compiler import Compiler
import re

from punica.exception.punica_exception import PunicaException, PunicaError

PYTHON_COMPILE_URL = "https://smartxcompiler.ont.io/api/beta/python/compile"


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
    def generate_abi_file(contract_path: str, save_path: str = ''):
        if save_path == '':
            split_path = os.path.split(contract_path)
            save_path = os.path.join(os.path.dirname(split_path[0]), 'build', split_path[1])
            save_path = save_path.replace('.py', '_abi.json')
        compiler = Compiler.load(contract_path)
        raw_avm = compiler.write()
        hex_str_hash = Digest.hash160(raw_avm, is_hex=True)
        byte_array_hash = bytearray(binascii.a2b_hex(hex_str_hash))
        byte_array_hash.reverse()
        contract_hash = byte_array_hash.hex()
        dict_abi = dict()
        dict_abi['hash'] = contract_hash
        dict_abi['entrypoint'] = compiler.entry_module.main.name
        dict_abi['functions'] = compiler.entry_module.abi.AbiFunclist
        json_data = json.dumps(dict_abi, indent=4)
        split_path = os.path.split(save_path)
        if not os.path.exists(split_path[0]):
            os.makedirs(split_path[0])
        with open(save_path, 'w') as f:
            f.write(json_data)

    @staticmethod
    def compile_contract(contract_path: str, local: bool = False, abi_save_path: str = '', avm_save_path: str = ''):
        if abi_save_path == '':
            split_path = os.path.split(contract_path)
            save_path = os.path.join(os.path.dirname(split_path[0]), 'build', split_path[1])
            abi_save_path = save_path.replace('.py', '_abi.json')
        if avm_save_path == '':
            split_path = os.path.split(contract_path)
            save_path = os.path.join(os.path.dirname(split_path[0]), 'build', split_path[1])
            avm_save_path = save_path.replace('.py', '.avm')
        if not local:
            PunicaCompiler.compile_contract_remote(contract_path)
            return
        try:
            PunicaCompiler.generate_avm_file(contract_path, avm_save_path)
            PunicaCompiler.generate_abi_file(contract_path, abi_save_path)
        except PermissionError as error:
            if error.args[0] == 13:
                raise PunicaException(PunicaError.permission_error)
            else:
                raise PunicaException(PunicaError.other_error(error.args[1]))

    @staticmethod
    def compile_contract_remote(contract_path: str):
        with open(contract_path, "r") as f:
            contract = f.read()
            dict_payload = dict()
            dict_payload['type'] = 'Python'
            dict_payload['code'] = contract
            url = PYTHON_COMPILE_URL
            header = {'Content-type': 'application/json'}
            timeout = 10
            path = os.path.dirname(contract_path)
            file_name = os.path.basename(contract_path).split(".")
            session = requests.session()
            res = session.post(url, json=dict_payload, headers=header, timeout=timeout, verify=False)
            result = json.loads(res.content.decode())
            if result["errcode"] == 0:
                with open(path + "/" + file_name[0] + ".avm", "w", encoding='utf-8') as f:
                    avm = result["avm"].lstrip('b\'')
                    temp = avm.rstrip('\'')
                    f.write(temp)
                with open(path + "/" + file_name[0] + "_abi.json", "w", encoding='utf-8') as f2:
                    r = re.sub('\\\\n', '', str(result["abi"]))
                    abi = str(r.lstrip('b\''))
                    temp = abi.rstrip('\'')
                    f2.write(temp.replace(' ', ''))
                print("compiled, Thank you")
            else:
                print("compile failed")
                print(result)

