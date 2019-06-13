#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import getpass

import crayons
from click import echo
from click._unicodefun import click
from ontology.exception.exception import SDKException
from ontology.sdk import Ontology
from ontology.common.address import Address

from punica.utils.file_system import (
    read_avm,
    read_wallet
)

from punica.utils.handle_config import (
    handle_network_config,
    handle_deploy_config
)

from punica.exception.punica_exception import PunicaException, PunicaError


class Deploy(object):
    @staticmethod
    def generate_signed_deploy_transaction(avm_code: str, project_path: str = '', wallet_file_name: str = '',
                                           config: str = '', password: str = ''):
        wallet_file, deploy_information = handle_deploy_config(project_path, config)
        if wallet_file_name != '':
            wallet_manager = read_wallet(project_path, wallet_file_name)
        else:
            wallet_manager = read_wallet(project_path, wallet_file)
        need_storage = deploy_information.get('needStorage', True)
        name = deploy_information.get('name', os.path.split(project_path)[1])
        version = deploy_information.get('version', '0.0.1')
        author = deploy_information.get('author', '')
        email = deploy_information.get('email', '')
        desc = deploy_information.get('desc', '')
        b58_payer_address = deploy_information.get('payer', wallet_manager.get_default_account_data().b58_address)
        if b58_payer_address == '':
            raise PunicaException(PunicaError.other_error('payer address should not be None'))
        gas_price = deploy_information.get('gasPrice', 500)
        gas_limit = deploy_information.get('gasLimit', 21000000)
        ontology = Ontology()
        tx = ontology.neo_vm.make_deploy_transaction(avm_code, need_storage, name, version, author, email, desc,
                                                     gas_price, gas_limit, b58_payer_address)
        payer_acct = wallet_manager.get_account_by_b58_address(b58_payer_address, password)
        if payer_acct is None:
            raise PunicaException(PunicaError.other_error(b58_payer_address + ' not found'))
        tx.sign_transaction(payer_acct)
        return tx

    @staticmethod
    def generate_contract_address(avm_dir_path: str = '', avm_file_name: str = '') -> str:
        if avm_dir_path == '':
            avm_dir_path = os.path.join(os.getcwd(), 'build', 'contracts')
        if not os.path.isdir(avm_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        hex_avm_code = read_avm(avm_dir_path, avm_file_name)[0]
        hex_contract_address = Address.from_avm_code(hex_avm_code).hex(little_endian=True)
        return hex_contract_address

    @staticmethod
    def check_deploy_state(tx_hash, project_path: str = '', network: str = ''):
        if project_path == '':
            project_path = os.getcwd()
        if not os.path.isdir(project_path):
            raise PunicaException(PunicaError.dir_path_error)
        rpc_address = handle_network_config(project_path, network, False)
        ontology = Ontology()
        ontology.rpc.set_address(rpc_address)
        time.sleep(8)
        tx = ontology.rpc.get_transaction_by_tx_hash(tx_hash)
        if tx == 'unknown transaction':
            return False
        else:
            return True

    @staticmethod
    def deploy_smart_contract(project_dir: str = '', network: str = '', avm_file_name: str = '',
                              wallet_file_name: str = '', config: str = '', password: str = '') -> str:
        if project_dir == '':
            project_dir = os.getcwd()
        if avm_file_name == '':
            avm_dir_path = os.path.join(project_dir, 'contracts', 'build')
        else:
            avm_path = os.path.join(project_dir, avm_file_name)
            if os.path.exists(avm_path):
                avm_dir_path = os.path.dirname(avm_path)
                avm_file_name = os.path.basename(avm_path)
            else:
                avm_dir_path = os.path.join(project_dir, 'contracts', 'build')
        if not os.path.exists(avm_dir_path):
            echo(crayons.red('No avm file found in this project', bold=True))
            return ''
        rpc_address = handle_network_config(project_dir, network)
        try:
            hex_avm_code, avm_file_name = read_avm(avm_dir_path, avm_file_name)
        except PunicaException as e:
            print(e.args)
            return ''
        if hex_avm_code == '':
            raise PunicaException(PunicaError.avm_file_empty)
        hex_contract_address = Deploy.generate_contract_address(avm_dir_path, avm_file_name)
        ontology = Ontology()
        ontology.rpc.set_address(rpc_address)
        try:
            contract = ontology.rpc.get_contract(hex_contract_address)
            echo('\tDeploy failed...')
            if len(contract.get('Code', '')) != 0:
                echo('\tThe contract has exist in current network...')
                echo('\tThe contract address is {}'.format(hex_contract_address))
            else:
                echo('\tSomething is error... ')
                echo(f'\t{contract}')
            return ''
        except SDKException as e:
            if 'unknow contract' in e.args[1]:
                pass
            elif 'ConnectionError' in e.args[1]:
                echo('\tNetwork error, please check your network first.')
                return ''
            else:
                raise e
        try:
            if len(password) == 0:
                password = getpass.getpass(prompt='Please input account password: ')
            tx = Deploy.generate_signed_deploy_transaction(hex_avm_code, project_dir, wallet_file_name, config,
                                                           password)
        except PunicaException as e:
            echo('\tDeploy failed...')
            echo('\t', e.args[1])
            return ''
        echo('Running deployment: {}'.format(avm_file_name))
        echo('\tDeploying...')
        ontology.rpc.set_address(rpc_address)
        tx_hash = ontology.rpc.send_raw_transaction(tx)
        echo('\tThe transaction has been sent to network...')
        echo(f'\tPlease check the status by TxHash: {tx_hash}')
        return tx_hash
