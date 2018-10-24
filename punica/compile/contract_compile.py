#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import binascii
import os

import requests
from boa.util import Digest
from boa.compiler import Compiler
import re

from punica.common.define import DEFAULT_CONFIG
from punica.exception.punica_exception import PunicaException, PunicaError

from requests.packages.urllib3.exceptions import InsecureRequestWarning

PYTHON_COMPILE_URL = "https://smartxcompiler.ont.io/api/beta/python/compile"
CSHARP_COMPILE_URL = "https://smartxcompiler.ont.io/api/v1.0/csharp/compile"


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
            if save_path.endswith('.py'):
                abi_save_path = save_path.replace('.py', '_abi.json')
            else:
                abi_save_path = save_path.replace('.cs', '_abi.json')
        if avm_save_path == '':
            split_path = os.path.split(contract_path)
            save_path = os.path.join(os.path.dirname(split_path[0]), 'build', split_path[1])
            if avm_save_path.endswith('.py'):
                avm_save_path = save_path.replace('.py', '.avm')
            else:
                avm_save_path = save_path.replace('.cs', '.avm')
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
            if contract_path.endswith('.py'):
                dict_payload['type'] = 'Python'
                dict_payload['code'] = contract
                url = PYTHON_COMPILE_URL
            else:
                dict_payload['type'] = 'CSharp'
                dict_payload['code'] = contract
                url = CSHARP_COMPILE_URL
            header = {'Content-type': 'application/json'}
            timeout = 10
            path = os.path.dirname(contract_path)
            file_name = os.path.basename(contract_path).split(".")
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            session = requests.session()
            res = session.post(url, json=dict_payload, headers=header, timeout=timeout, verify=False)
            result = json.loads(res.content.decode())
            if result["errcode"] == 0:
                avm_save_path = os.path.join(path, 'build', file_name[0] + ".avm")
                if not os.path.exists(os.path.join(path, 'build')):
                    os.makedirs(os.path.join(path, 'build'))
                with open(avm_save_path, "w", encoding='utf-8') as f:
                    avm = result["avm"].lstrip('b\'')
                    temp = avm.rstrip('\'')
                    f.write(temp)
                abi_save_path = os.path.join(path, 'build', file_name[0] + "_abi.json")
                with open(abi_save_path, "w", encoding='utf-8') as f2:
                    r = re.sub('\\\\n', '', str(result["abi"]))
                    abi = str(r.lstrip('b\''))
                    temp = abi.rstrip('\'')
                    f2.write(temp.replace(' ', ''))
                print("compiled, Thank you")
                invoke_config_path = os.path.join(path, DEFAULT_CONFIG)
                if os.path.exists(invoke_config_path):
                    PunicaCompiler.update_invoke_config(abi_save_path, invoke_config_path)
                else:
                    PunicaCompiler.generate_invoke_config(abi_save_path, invoke_config_path)
            else:
                print("compile failed")
                print(result)

    @staticmethod
    def generate_invoke_config(abi_path: str, invoke_config_path: str):
        if abi_path == '':
            raise PunicaError.abi_file_not_found
        with open(abi_path, "r") as f:
            abi_content = f.read()
        dict_abi = json.loads(abi_content)
        dict_invoke = dict()
        dict_invoke['defaultWallet'] = ''
        dict_deploy = dict()
        dict_deploy['name'] = ''
        dict_deploy['version'] = ''
        dict_deploy['author'] = ''
        dict_deploy['email'] = ''
        dict_deploy['desc'] = ''
        dict_deploy['needStorage'] = True
        dict_deploy['payer'] = ''
        dict_deploy['gasPrice'] = 500
        dict_deploy['gasLimit'] = 21000000
        dict_invoke['deployConfig'] = dict_deploy
        dict_invoke_detail = dict()
        dict_invoke_detail['abi'] = os.path.basename(abi_path)
        dict_invoke_detail['defaultPayer'] = ''
        dict_invoke_detail['gasPrice'] = 500
        dict_invoke_detail['gasLimit'] = 20000
        dict_invoke_functions = list()
        for func in dict_abi['functions']:
            if func['name'] == 'Main':
                continue
            dict_func_info = dict()
            dict_param = dict()
            if len(func['parameters']) != 0:
                for param in func['parameters']:
                    if param['name'] == '':
                        continue
                    dict_param[param['name']] = ''
            dict_func_info['name'] = func['name']
            dict_func_info['params'] = dict_param
            dict_func_info['signers'] = dict()
            dict_func_info['preExec'] = True
            dict_invoke_functions.append(dict_func_info)
        dict_invoke_detail['functions'] = dict_invoke_functions
        dict_invoke['invokeConfig'] = dict_invoke_detail
        with open(invoke_config_path, "w") as f:
            json.dump(dict_invoke, f, default=lambda obj: dict(obj), indent=4)

    @staticmethod
    def update_invoke_config(abi_path: str, invoke_config_path: str):
        with open(invoke_config_path, 'r') as f:
            invoke_content = f.read()
        dict_invoke = json.loads(invoke_content)
        with open(abi_path, 'r') as f:
            abi_content = f.read()
        dict_abi = json.loads(abi_content)
        if len(dict_abi['functions']) == 0:
            return
        is_need_update = False
        all_funcs = dict_invoke['invokeConfig']['functions']
        all_func_name_list = list()
        for func_information in all_funcs:
            all_func_name_list.append(func_information['name'])
        for func in dict_abi['functions']:
            if func['name'] not in all_func_name_list:
                if func['name'] == 'Main':
                    continue
                is_need_update = True
                dict_func_info = dict()
                dict_param = dict()
                if len(func['parameters']) != 0:
                    for param in func['parameters']:
                        if param['name'] == '':
                            continue
                        dict_param[param['name']] = ''
                dict_func_info['name'] = func['name']
                dict_func_info['params'] = dict_param
                dict_func_info['signers'] = dict()
                dict_func_info['preExec'] = True
                dict_invoke['invokeConfig']['functions'].append(dict_func_info)
        if is_need_update:
            with open(invoke_config_path, 'w') as f:
                json.dump(dict_invoke, f, default=lambda obj: dict(obj), indent=4)


