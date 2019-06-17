#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import stat
import shutil

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


def ensure_remove_dir_if_exists(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=False, onerror=handle_read_only_remove_error)
        return True
    return False


def save_avm_file(avm_code: str, to_path: str):
    try:
        with open(to_path, 'w') as f:
            f.write(avm_code.lstrip('b\'').rstrip('\''))
    except PermissionError as error:
        if error.args[0] == 13:
            raise PunicaException(PunicaError.permission_error)
        else:
            raise PunicaException(PunicaError.other_error(error.args[1]))


def read_avm(avm_dir_path: str, avm_file_name: str = '') -> (str, str):
    if not os.path.isdir(avm_dir_path):
        raise PunicaException(PunicaError.directory_error)
    if avm_file_name != '':
        avm_file_path = os.path.join(avm_dir_path, avm_file_name)
        if not os.path.exists(avm_file_path):
            raise PunicaException(PunicaError.other_error(avm_file_path + ' not exist'))
        with open(avm_file_path, 'r') as f:
            hex_avm = f.read()
    else:
        dir_list = os.listdir(avm_dir_path)
        hex_avm = ''
        for file in dir_list:
            split_path = os.path.splitext(file)
            if (split_path[0] == avm_file_name or avm_file_name == '') and split_path[1] == '.avm':
                avm_file_name = ''.join(split_path)
                avm_path = os.path.join(avm_dir_path, file)
                with open(avm_path, 'r') as f:
                    hex_avm = f.read()
                    break
    return hex_avm, avm_file_name


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
    except SDKException as e:
        raise PunicaException(PunicaError.wallet_file_error)
    return wallet_manager
