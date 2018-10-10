#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import getpass
import os
import time

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_vm import NeoVm
from ontology.wallet.wallet_manager import WalletManager

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
    def generate_signed_invoke_transaction(contract_address: bytearray, abi_func: AbiFunction, payer_acct: Account,
                                           signers: list, gas_price: int, gas_limit: int):
        params = BuildParams.serialize_abi_function(abi_func)
        unix_time_now = int(time.time())
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        signers_len = len(signers)
        payer_address = payer_acct.get_address().to_array()
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_address, params,
                         bytearray(), [], bytearray())
        ontology = OntologySdk()
        if signers_len == 1:
            ontology.sign_transaction(tx, signers[0])
        else:
            for index in range(signers_len):
                OntologySdk().add_sign_transaction(tx, signers[index])
        return tx

    @staticmethod
    def generate_unsigned_invoke_transaction(abi_func: AbiFunction, contract_address: bytearray, gas_price: int,
                                             gas_limit: int):
        params = BuildParams.serialize_abi_function(abi_func)
        tx = NeoVm.make_invoke_transaction(contract_address, bytearray(params), b'', gas_limit, gas_price)
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
    def params_normalize(params: list) -> list:
        for index in range(len(params)):
            param = params[index]
            if isinstance(param, list):
                for i in range(len(param)):
                    if isinstance(param[i], str) and len(param[i]) == 34:
                        try:
                            param[i] = Address.b58decode(param[i]).to_array()
                        except SDKException:
                            pass
                params[index] = param
            else:
                if isinstance(params[index], str) and len(params[index]) == 34:
                    try:
                        params[index] = Address.b58decode(params[index]).to_array()
                    except SDKException:
                        pass
        return params

    @staticmethod
    def invoke_all_function_in_list(wallet_file_name: str = '', project_dir_path: str = '', network: str = ''):
        if project_dir_path == '':
            project_dir_path = os.getcwd()
        if not os.path.isdir(project_dir_path):
            raise PunicaException(PunicaError.dir_path_error)

        wallet_dir_path = os.path.join(project_dir_path, 'wallet')
        wallet_manager = read_wallet(wallet_dir_path, wallet_file_name)

        rpc_address = handle_network_config(project_dir_path, network)
        ontology = OntologySdk()
        ontology.rpc.set_address(rpc_address)

        invoke_config = handle_invoke_config(project_dir_path)
        try:
            abi_file_name = invoke_config['abi']
        except KeyError:
            raise PunicaException(PunicaError.config_file_error)
        try:
            default_b58_payer_address = invoke_config['defaultPayer']
        except KeyError:
            raise PunicaException(PunicaError.config_file_error)
        print('Running invocation: {}'.format(abi_file_name))
        abi_dir_path = os.path.join(project_dir_path, 'build')
        dict_abi = read_abi(abi_dir_path, abi_file_name)
        try:
            hex_contract_address = dict_abi['hash']
        except KeyError:
            raise PunicaException(PunicaError.abi_file_error)

        if not isinstance(hex_contract_address, str) or len(hex_contract_address) != 40:
            raise PunicaException(PunicaError.abi_file_error)
        contract = ontology.rpc.get_smart_contract(hex_contract_address)
        if contract == 'unknow contract':
            print('Contract 0x{} hasn\'t been deployed in current network: {}'.format(hex_contract_address, network))
            raise PunicaException(PunicaError.abi_file_error)
        contract_address = bytearray(binascii.a2b_hex(hex_contract_address))
        contract_address.reverse()
        abi_info = Invoke.generate_abi_info(dict_abi)
        gas_price = invoke_config.get('gasPrice', 500)
        gas_limit = invoke_config.get('gasLimit', 21000000)
        invoke_function_dict = invoke_config.get('Functions', dict())
        print('Unlock default payer account...')
        default_payer_acct = Invoke.unlock_account(default_b58_payer_address, wallet_manager)
        for function_key in invoke_function_dict:
            print('Invoking {}...'.format(function_key))
            abi_function = abi_info.get_function(function_key)
            function_information = invoke_function_dict[function_key]
            try:
                params = function_information['params']
                params = Invoke.params_normalize(params)
                if len(abi_function.parameters) == 0:
                    pass
                elif len(abi_function.parameters) == 1:
                    abi_function.set_params_value((params,))
                elif len(abi_function.parameters) == len(params):
                    abi_function.set_params_value(tuple(params))
                else:
                    abi_function = None
                    print('\tInvoke failed, params mismatching with the abi file')
                if abi_function is not None:
                    b58_signers = function_information.get('signers', list())
                    if len(b58_signers) == 0:
                        tx = Invoke.generate_unsigned_invoke_transaction(abi_function, contract_address, gas_price,
                                                                         gas_limit)
                        result = ontology.rpc.send_raw_transaction_pre_exec(tx)
                        print('\tInvoke successful...')
                        print('\t\t... Invoke result: {}'.format(result))
                    else:
                        b58_payer_address = function_information.get('payer', default_b58_payer_address)
                        if b58_payer_address == default_b58_payer_address:
                            payer_acct = default_payer_acct
                        else:
                            payer_acct = Invoke.unlock_account(b58_payer_address, wallet_manager)
                        b58_signers = function_information.get('signers', list())
                        signer_list = list()
                        if len(b58_signers) != 0:
                            print('Unlock signers account...')
                            for b58_signer_address in b58_signers:
                                signer = Invoke.unlock_account(b58_signer_address, wallet_manager)
                                signer_list.append(signer)
                        tx = Invoke.generate_signed_invoke_transaction(contract_address, abi_function, payer_acct,
                                                                       signer_list, gas_price, gas_limit)
                        ontology.rpc.set_address(rpc_address)
                        try:
                            tx_hash = ontology.rpc.send_raw_transaction(tx)
                            if tx_hash == '':
                                print('\tInvoke failed...')
                            else:
                                print('\tInvoke successful...')
                                print('\t\t... txHash: 0x{}'.format(tx_hash))
                        except SDKException as e:
                            print('\tInvoke failed, {}'.format(e.args[1].replace('Other Error, ', '')))

            except KeyError:
                print('\tInvoke failed, params is empty')
