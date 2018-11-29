#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import getpass
import os
import time

from ontology.common.address import Address
from ontology.exception.exception import SDKException
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_vm import NeoVm
from ontology.wallet.wallet_manager import WalletManager

from punica.common.define import DEFAULT_CONFIG
from punica.exception.punica_exception import PunicaException, PunicaError

from punica.utils.file_system import (
    read_abi,
    read_wallet
)

from punica.utils.handle_config import (
    handle_invoke_config,
    handle_network_config
)


class Invoke:
    @staticmethod
    def get_function(params: dict, function_name: str, abi_info: AbiInfo):
        if function_name == '':
            raise PunicaException(PunicaError.other_error('function_name should not be nil'))
        params = Invoke.params_normalize(params)
        abi_function = abi_info.get_function(function_name)
        if len(abi_function.parameters) == 0:
            pass
        elif len(abi_function.parameters) == 1:
            abi_function.set_params_value((params,))
        elif len(abi_function.parameters) == len(params):
            abi_function.set_params_value(tuple(params))
        return abi_function

    @staticmethod
    def list_all_functions(project_dir: str, config_name: str):
        if config_name == '':
            config_name = DEFAULT_CONFIG
        try:
            wallet_file, invoke_config, password_config = handle_invoke_config(project_dir, config_name)
        except Exception as e:
            print(e.args)
            return
        try:
            abi_file_name = invoke_config['abi']
        except KeyError:
            raise PunicaException(PunicaError.config_file_error)
        abi_dir_path = os.path.join(project_dir, 'contracts', 'build')
        try:
            dict_abi = read_abi(abi_dir_path, abi_file_name)
        except PunicaException as e:
            print(e.args)
            return
        try:
            func_in_abi_list = dict_abi['functions']
        except KeyError:
            raise PunicaException(PunicaError.other_error('abi file is wrong'))
        func_name_in_abi_list = list()
        for func_in_abi_dict in func_in_abi_list:
            try:
                func_name = func_in_abi_dict['name']
            except KeyError:
                raise PunicaException(PunicaError.other_error('abi file is wrong'))
            func_name_in_abi_list.append(func_name)
        print("All Functions:")
        invoke_function_list = invoke_config['functions']
        for function_information in invoke_function_list:
            if function_information['operation'] in func_name_in_abi_list:
                print('\t', function_information['operation'])

    @staticmethod
    def generate_abi_info(dict_abi: dict) -> AbiInfo:
        try:
            contract_address = dict_abi['hash']
            functions = dict_abi['functions']
        except KeyError:
            raise PunicaException(PunicaError.abi_file_error)
        entry_point = dict_abi.get('entrypoint', '')
        events = dict_abi.get('events', list())
        abi_info = AbiInfo(contract_address, entry_point, functions, events)
        return abi_info

    @staticmethod
    def generate_unsigned_invoke_transaction(contract_address: bytearray, params_list: list, payer_base58: bytearray, gas_price: int,
                                             gas_limit: int):
        # params = BuildParams.serialize_abi_function(abi_func)
        params = BuildParams.create_code_params_script(params_list)
        tx = NeoVm.make_invoke_transaction(contract_address, bytearray(params), payer_base58, gas_limit, gas_price)
        return tx

    @staticmethod
    def get_invoke_dict(abi_file_name: str, project_path: str = ''):
        if project_path == '':
            project_path = os.getcwd()
        if not os.path.isdir(project_path):
            raise PunicaException(PunicaError.dir_path_error)
        abi_dir_path = os.path.join(project_path, 'build')
        dict_abi = read_abi(abi_dir_path, abi_file_name)
        if len(dict_abi) == 0:
            raise PunicaException(PunicaError.abi_file_empty)
        return dict_abi

    @staticmethod
    def unlock_account(b58_address: str, wallet_manager: WalletManager):
        print('\tUnlock account: {}'.format(b58_address))
        while True:
            try:
                acct_password = getpass.getpass('\tPlease input account password: ')
                acct = wallet_manager.get_account(b58_address, acct_password)
                print('\tUnlock successful...')
                break
            except AssertionError:
                print('\tPassword uncorrected...')
        return acct

    @staticmethod
    def generate_signer_acct_list(b58_signers: list, wallet_manager: WalletManager):
        print('Unlock signer accounts...')
        signer_acct_list = list()
        for b58_signer in b58_signers:
            while True:
                try:
                    print('\tUnlock signer account {}...'.format(b58_signer))
                    signer_password = getpass.getpass('\tPlease input account password: ')
                    signer = wallet_manager.get_account(b58_signer, signer_password)
                    signer_acct_list.append(signer)
                    print('\tUnlock successful...')
                    break
                except AssertionError:
                    print('\tPassword uncorrected...')
        return signer_acct_list

    @staticmethod
    def get_account(ontology, password_config, b58_address):
        if len(password_config) != 0:
            pwd = password_config.get(b58_address, '')
            if pwd != '':
                return ontology.wallet_manager.get_account(b58_address, pwd)
        return Invoke.unlock_account(b58_address, ontology.wallet_manager)

    @staticmethod
    def params_build(func_name: str, params: list) -> list:
        params_list = list()
        params_list.append(func_name.encode())
        temp_list = list()
        for param in params:
            if isinstance(param, list):
                temp_param_list = []
                for p in param:
                    temp_param_list.append(p)
                temp_list.append(temp_param_list)
            else:
                temp_list.append(param)
        params_list.append(temp_list)
        return params_list

    @staticmethod
    def params_normalize2(list_param: list):
        list_params = list()
        for param in list_param:
            if isinstance(param, dict):
                item = param.get('value', '')
                if isinstance(item, bool):
                    list_params.append(item)
                elif isinstance(item, int):
                    list_params.append(item)
                elif isinstance(item, str):
                    list_params.append(Invoke.handle_param_str2(item))
                elif isinstance(item, list):
                    list_temp = list()
                    for i in item:
                        list_temp.append(Invoke.parse_param(i))
                    list_params.append(list_temp)
                elif isinstance(item, dict):
                    dict_temp = dict()
                    for k, v in item.items():
                        dict_temp[k] = Invoke.parse_param(v)
                    list_params.append(dict_temp)
                else:
                    raise PunicaException(PunicaError.other_error('not support data type'))
        return list_params

    @staticmethod
    def parse_param(param):
        if isinstance(param, bool):
            return param
        elif isinstance(param, int):
            return param
        elif isinstance(param, str):
            return Invoke.handle_param_str2(param)
        elif isinstance(param, list):
            list_temp = list()
            for i in param:
                list_temp.append(Invoke.parse_param(i))
            return list_temp
        elif isinstance(param, dict):
            dict_temp = dict()
            for k, v in param.items():
                dict_temp[k] = Invoke.parse_param(v)
            return dict_temp
        else:
            raise PunicaException(PunicaError.other_error('not support data type'))

    @staticmethod
    def params_normalize(dict_params: dict) -> list:
        list_params = list()
        isfirst = False
        if len(dict_params) == 0:
            return list_params
        for param in dict_params.values():
            if isinstance(param, list):
                if len(param) == 0:
                    continue
                temp_params_list = list()
                for i in range(len(param)):
                    if isinstance(param[i], dict):
                        list_params2 = list()
                        for p in param[i].values():
                            if isinstance(p, str):
                                Invoke.handle_param_str(list_params2, p)
                            elif isinstance(p, int):
                                list_params2.append(p)
                        temp_params_list.append(list_params2)
                    elif isinstance(param[i], int):
                        isfirst = True
                        temp_params_list.append(param[i])
                    elif isinstance(param[i], str):
                        isfirst = True
                        Invoke.handle_param_str(temp_params_list, param[i])
                    else:
                        raise PunicaException(PunicaError.parameter_type_error)
                if len(temp_params_list) >= 2 and isfirst:
                    list_params.append(temp_params_list)
                else:
                    list_params = temp_params_list
            elif isinstance(param, str):
                if param == '':
                    raise PunicaException(PunicaError.parameter_type_error)
                Invoke.handle_param_str(list_params, param)
            elif isinstance(param, int):
                list_params.append(param)
        return list_params

    @staticmethod
    def handle_param_str2(p: str):
        list_p = p.split(':')
        if len(list_p) != 2:
            raise PunicaException(PunicaError.parameter_type_error)
        if list_p[0] == 'ByteArray':
            return bytearray.fromhex(list_p[1])
        elif list_p[0] == 'String':
            return list_p[1]
        elif list_p[0] == 'Address':
            return Address.b58decode(list_p[1]).to_array()
        else:
            raise PunicaException(PunicaError.parameter_type_error)

    @staticmethod
    def handle_param_str(list_params2: list, p: str):
        list_p = p.split(':')
        if len(list_p) != 2:
            raise PunicaException(PunicaError.parameter_type_error)
        if list_p[0] == 'ByteArray':
            if len(list_p[1]) == 34:
                list_params2.append(Address.b58decode(list_p[1]).to_array())
            else:
                list_params2.append(list_p[1].encode())
        elif list_p[0] == 'String':
            list_params2.append(list_p[1])
        elif list_p[0] == 'Address':
            list_params2.append(Address.b58decode(list_p[1]).to_array())
        elif list_p[0] == 'Hex':
            list_params2.append(bytearray.fromhex(list_p[1]))
        else:
            raise PunicaException(PunicaError.parameter_type_error)

    @staticmethod
    def invoke_all_function_in_list(wallet_file_name: str = '', project_dir_path: str = '', network: str = '',
                                    exec_func_str: str = '', config_name: str = '', pre_exec: str = ''):
        if project_dir_path == '':
            project_dir_path = os.getcwd()
        if not os.path.isdir(project_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        try:
            wallet_file, invoke_config, password_config = handle_invoke_config(project_dir_path, config_name)
            sleep_time = invoke_config.get('sleepTime', 6)
        except PunicaException as e:
            print(e.args)
            return
        ontology = OntologySdk()
        rpc_address = handle_network_config(project_dir_path, network)
        ontology.rpc.set_address(rpc_address)
        if wallet_file_name != '':
            ontology.wallet_manager = read_wallet(project_dir_path, wallet_file_name)
        else:
            ontology.wallet_manager = read_wallet(project_dir_path, wallet_file)
        try:
            abi_file_name = invoke_config['abi']
        except KeyError:
            raise PunicaException(PunicaError.config_file_error)
        try:
            default_b58_payer_address = invoke_config['defaultPayer']
        except KeyError:
            raise PunicaException(PunicaError.other_error("defaultPayer is null"))
        print('Running invocation: {}'.format(abi_file_name))
        abi_dir_path = os.path.join(project_dir_path, 'contracts', 'build')
        dict_abi = read_abi(abi_dir_path, abi_file_name)
        try:
            hex_contract_address = dict_abi['hash']
        except KeyError:
            raise PunicaException(PunicaError.abi_file_error)

        if not isinstance(hex_contract_address, str) or len(hex_contract_address) != 40:
            raise PunicaException(PunicaError.abi_file_error)
        contract = ontology.rpc.get_smart_contract(hex_contract_address)
        if contract == 'unknow contracts':
            print('Contract 0x{} hasn\'t been deployed in current network: {}'.format(hex_contract_address, network))
            raise PunicaException(PunicaError.abi_file_error)
        contract_address = bytearray(binascii.a2b_hex(hex_contract_address))
        contract_address.reverse()
        abi_info = Invoke.generate_abi_info(dict_abi)
        gas_price = invoke_config.get('gasPrice', 500)
        gas_limit = invoke_config.get('gasLimit', 21000000)
        invoke_function_list = invoke_config.get('functions', list())
        invoke_function_name_list = list()
        for invoke_function in invoke_function_list:
            invoke_function_name_list.append(invoke_function['operation'])
        all_exec_func_list = list()
        if exec_func_str != '':
            all_exec_func_list = exec_func_str.split(',')
        if default_b58_payer_address != '':
            print('Unlock default payer account...')
            default_payer_acct = Invoke.get_account(ontology, password_config, default_b58_payer_address)
        if len(all_exec_func_list) == 0:
            all_exec_func_list = invoke_function_name_list
        for function_name in all_exec_func_list:
            if function_name not in invoke_function_name_list:
                print('there is not the function:', '\"' + function_name + '\"' + ' in the default-config file')
                continue
            print('Invoking ', function_name)
            abi_function = abi_info.get_function(function_name)
            if abi_function is None:
                raise PunicaException(PunicaError.other_error('\"' + function_name + '\"' + 'not found in the abi file'))
            function_information = None
            for invoke_function in invoke_function_list:
                if invoke_function['operation'] == function_name:
                    function_information = invoke_function
                    break
            if function_information is None:
                print('there is not the function: ', function_name)
                return
            try:
                paramList = function_information['args']
                try:
                    # params = Invoke.params_normalize(paramsList)
                    params = Invoke.params_normalize2(paramList)
                    params_list = Invoke.params_build(function_name, params)
                except PunicaException as e:
                    print(e.args)
                    return
                # if len(abi_function.parameters) == 0:
                #     pass
                # elif len(abi_function.parameters) == 1:
                #     abi_function.set_params_value(tuple(params))
                # elif len(abi_function.parameters) == len(params):
                #     abi_function.set_params_value(tuple(params))
                # else:
                #     abi_function = None
                #     print('\tInvoke failed, params mismatching with the abi file')
                if abi_function is not None:
                    if (function_information['preExec'] and pre_exec == '') or (pre_exec == 'true'):
                        tx = Invoke.generate_unsigned_invoke_transaction(contract_address, params_list, bytearray(),
                                                                         gas_price, gas_limit)
                        result = ontology.rpc.send_raw_transaction_pre_exec(tx)
                        print('Invoke successful')
                        if isinstance(result, list):
                            print('Invoke result: {}'.format(result))
                            # print('Invoke result: {}'.format(list(map(lambda r: "0x" + r, result))))
                        else:
                            if result is None:
                                print('Invoke result: {}'.format(''))
                            else:
                                print('Invoke result: {}'.format(result))
                    else:
                        b58_payer_address = function_information.get('payer', default_b58_payer_address)
                        if default_b58_payer_address != '' and b58_payer_address == default_b58_payer_address:
                            payer_acct = default_payer_acct
                        else:
                            payer_acct = Invoke.get_account(ontology, password_config, b58_payer_address)
                        if payer_acct is None or payer_acct == '':
                            print('defaultPayer is None in invokeConfig')
                            return
                        tx = Invoke.generate_unsigned_invoke_transaction(contract_address, params_list,
                                                                         payer_acct.get_address().to_array(), gas_price,
                                                                         gas_limit)
                        ontology.add_sign_transaction(tx, payer_acct)
                        dict_signers = function_information.get('signature', dict())
                        signer_list = list()
                        if len(dict_signers) != 0:
                            print('Unlock signers account...')
                            for b58_signer_address in dict_signers['signers']:
                                if b58_signer_address == b58_payer_address:
                                    signer_list.append(payer_acct)
                                    continue
                                else:
                                    signer = Invoke.get_account(ontology, password_config, b58_signer_address)
                                    signer_list.append(signer)
                            if dict_signers['m'] == 1:
                                for signer in signer_list:
                                    ontology.add_sign_transaction(tx, signer)
                            elif dict_signers['m'] > 1:
                                list_public_key = list()
                                for pubkey in dict_signers['publicKeys']:
                                    list_public_key.append(bytearray.fromhex(pubkey))
                                for signer in signer_list:
                                    ontology.add_multi_sign_transaction(tx, dict_signers['m'], list_public_key, signer)
                        ontology.rpc.set_address(rpc_address)
                        try:
                            tx_hash = ontology.rpc.send_raw_transaction(tx)
                            time.sleep(sleep_time)
                            if tx_hash == '':
                                print('Invoke failed...')
                                print('txHash: 0x{}'.format(tx.hash256_explorer()))
                            else:
                                print('Invoke successful')
                                print('txHash: 0x{}'.format(tx_hash))
                        except SDKException as e:
                            print('txHash: 0x{}'.format(tx.hash256_explorer()))
                            print('\tInvoke failed, {}'.format(e.args[1].replace('Other Error, ', '')))

            except (KeyError, RuntimeError) as e:
                print('\tInvoke failed,', e.args)
