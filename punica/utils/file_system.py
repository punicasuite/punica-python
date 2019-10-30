#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import stat
import shutil
from os import path

from ontology.exception.exception import SDKException
from ontology.wallet.wallet_manager import WalletManager

from punica.exception.punica_exception import PunicaException, PunicaError


def ensure_path_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return True
    return False


def ensure_file_exists(file_path):
    if os.path.exists(file_path):
        return False
    base_dir = os.path.dirname(file_path)
    ensure_path_exists(base_dir)
    with open(file_path, 'w'):
        pass
    return True


def handle_read_only_remove_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_file_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False


def remove_dir_if_exists(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        return True
    return False


def ensure_remove_dir_if_exists(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path, ignore_errors=False, onerror=handle_read_only_remove_error)
        return True
    return False


def read_avm_code(avm_dir: str, contract_name: str):
    if not contract_name.endswith('.avm'):
        contract_name = ''.join([contract_name, '.avm'])
    avm_file_path = path.join(avm_dir, contract_name)
    if not path.exists(avm_file_path):
        raise PunicaException(PunicaError.avm_file_not_found)
    with open(avm_file_path, 'r') as f:
        avm_code = f.read()
    if len(avm_code) == 0:
        raise PunicaException(PunicaError.avm_file_empty)
    return avm_code


def save_avm_file(avm_code: str, to_path: str):
    try:
        with open(to_path, 'w') as f:
            f.write(avm_code.lstrip('b\'').rstrip('\''))
    except PermissionError as error:
        if error.args[0] == 13:
            raise PunicaException(PunicaError.permission_error)
        else:
            raise PunicaException(PunicaError.other_error(error.args[1]))


def read_abi(abi_dir_path: str, abi_file_name: str) -> dict:
    if not os.path.isdir(abi_dir_path):
        raise PunicaException(PunicaError.other_error('build folder not exist, please compile first'))
    abi_file_path = os.path.join(abi_dir_path, abi_file_name)
    if not os.path.exists(abi_file_path):
        raise PunicaException(PunicaError.other_error('abi config file not exist'))
    with open(abi_file_path, 'r') as f:
        dict_abi = json.load(f)
    return dict_abi


def read_wallet(project_path: str, wallet_file_name: str = '') -> WalletManager:
    if not os.path.isdir(project_path):
        raise PunicaException(PunicaError.directory_error)
    wallet_manager = WalletManager()
    if wallet_file_name == '' or wallet_file_name == '"':
        wallet_dir_path = os.path.join(project_path, 'wallet')
        dir_list = os.listdir(wallet_dir_path)
        if len(dir_list) == 1:
            wallet_path = os.path.join(wallet_dir_path, dir_list[0])
        elif os.path.exists(os.path.join(wallet_dir_path, 'wallet.json')):
            print('Use the default wallet file: wallet.json')
            wallet_path = os.path.join(wallet_dir_path, 'wallet.json')
        else:
            raise PunicaException(PunicaError.wallet_file_unspecified)
    else:
        wallet_path = os.path.join(project_path, wallet_file_name)
        if not os.path.exists(wallet_path):
            if os.path.dirname(wallet_file_name) != '':
                raise PunicaException(PunicaError.other_error(wallet_file_name + ' not found'))
            wallet_path = os.path.join(project_path, 'wallet', wallet_file_name)
            if not os.path.exists(wallet_path):
                raise PunicaException(PunicaError.other_error(''.join([wallet_path, ' is error'])))
    try:
        wallet_manager.open_wallet(wallet_path)
    except SDKException:
        raise PunicaException(PunicaError.wallet_file_error)
    return wallet_manager
