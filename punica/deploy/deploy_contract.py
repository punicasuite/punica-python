#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import getpass

from ontology.common.address import Address
from ontology.ont_sdk import OntologySdk

from punica.utils.file_system import (
    read_avm,
    read_wallet
)

from punica.utils.handle_config import (
    handle_network_config,
    handle_deploy_config
)

from punica.exception.punica_exception import PunicaException, PunicaError


class Deploy:
    @staticmethod
    def generate_signed_deploy_transaction(hex_avm_code: str, project_path: str = '', wallet_file_name: str = '',
                                           config: str = ''):
        wallet_manager = read_wallet(project_path, wallet_file_name)
        deploy_information, password_information = handle_deploy_config(project_path, config)
        need_storage = deploy_information.get('needStorage', True)
        name = deploy_information.get('name', os.path.split(project_path)[1])
        version = deploy_information.get('version', '0.0.1')
        author = deploy_information.get('author', '')
        email = deploy_information.get('email', '')
        desc = deploy_information.get('desc', '')
        b58_payer_address = deploy_information.get('payer', wallet_manager.get_default_account().get_address())
        gas_limit = deploy_information.get('gasLimit', 21000000)
        gas_price = deploy_information.get('gasPrice', 500)
        ontology = OntologySdk()
        tx = ontology.neo_vm().make_deploy_transaction(hex_avm_code, need_storage, name, version, author, email,
                                                       desc, b58_payer_address, gas_limit, gas_price)
        password = password_information.get(b58_payer_address, '')
        if password == '':
            password = getpass.getpass('\tPlease input payer account password: ')
        payer_acct = wallet_manager.get_account(b58_payer_address, password)
        ontology.sign_transaction(tx, payer_acct)
        return tx

    @staticmethod
    def generate_contract_address(avm_dir_path: str = '', avm_file_name: str = '') -> str:
        if avm_dir_path == '':
            avm_dir_path = os.path.join(os.getcwd(), 'build', 'contracts')
        if not os.path.isdir(avm_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        hex_avm_code = read_avm(avm_dir_path, avm_file_name)[0]
        hex_contract_address = Address.address_from_vm_code(hex_avm_code).to_reverse_hex_str()
        return hex_contract_address

    @staticmethod
    def check_deploy_state(tx_hash, project_path: str = '', network: str = ''):
        if project_path == '':
            project_path = os.getcwd()
        if not os.path.isdir(project_path):
            raise PunicaException(PunicaError.dir_path_error)
        rpc_address = handle_network_config(project_path, network, False)
        ontology = OntologySdk()
        ontology.rpc.set_address(rpc_address)
        time.sleep(6)
        tx = ontology.rpc.get_raw_transaction(tx_hash)
        if tx == 'unknown transaction':
            return False
        else:
            return True

    @staticmethod
    def deploy_smart_contract(project_dir: str = '', network: str = '', avm_file_name: str = '',
                              wallet_file_name: str = '', config: str = ''):
        if project_dir == '':
            project_dir = os.getcwd()
        if avm_file_name != '':
            avm_path = os.path.join(project_dir, avm_file_name)
            if os.path.exists(avm_path):
                avm_dir_path = os.path.dirname(avm_path)
                avm_file_name = os.path.basename(avm_path)
            else:
                avm_dir_path = os.path.join(project_dir, 'contracts', 'build')
        else:
            avm_dir_path = os.path.join(project_dir, 'contracts', 'build')
        if not os.path.exists(avm_dir_path):
            print('there is not the avm file, please compile first')
            return
        rpc_address = handle_network_config(project_dir, network)
        try:
            hex_avm_code, avm_file_name = read_avm(avm_dir_path, avm_file_name)
        except PunicaException as e:
            print(e.args)
            return
        if hex_avm_code == '':
            raise PunicaException(PunicaError.avm_file_empty)
        hex_contract_address = Deploy.generate_contract_address(avm_dir_path, avm_file_name)
        ontology = OntologySdk()
        ontology.rpc.set_address(rpc_address)
        contract = ontology.rpc.get_smart_contract(hex_contract_address)
        if contract == 'unknow contract' or contract == 'unknow contracts':
            tx = Deploy.generate_signed_deploy_transaction(hex_avm_code, project_dir, wallet_file_name, config)
            print('Running deployment: {}'.format(avm_file_name))
            print('\tDeploying...')
            ontology.rpc.set_address(rpc_address)
            tx_hash = ontology.rpc.send_raw_transaction(tx)
            return tx_hash
        else:
            print('\tDeploy failed...')
            print('\tContract has been deployed...')
            print('\tContract address is {}'.format(hex_contract_address))
