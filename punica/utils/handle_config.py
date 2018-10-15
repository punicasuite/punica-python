#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

from punica.exception.punica_exception import PunicaException, PunicaError


def handle_network_config(config_dir_path: str, network: str = '', is_print: bool = True) -> str:
    try:
        config_file_path = os.path.join(config_dir_path, 'punica-config.json')
        with open(config_file_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise PunicaException(PunicaError.config_file_not_found)
    try:
        network_dict = config['networks']
    except KeyError:
        raise PunicaException(PunicaError.config_file_error)
    if network == '':
        try:
            network = list(network_dict.keys())[0]
        except IndexError:
            raise PunicaException(PunicaError.config_file_error)
    try:
        rpc_address = ''.join([network_dict[network]['host'], ':', str(network_dict[network]['port'])])
    except KeyError:
        raise PunicaException(PunicaError.config_file_error)
    if is_print:
        print('Using network \'{}\'.\n'.format(network))
    return rpc_address


def handle_deploy_config(config_dir_path: str) -> dict:
    try:
        config_file_path = os.path.join(config_dir_path, 'punica-config.json')
        with open(config_file_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise PunicaException(PunicaError.config_file_not_found)
    try:
        deploy_information = config['invokeConfig']
    except KeyError:
        raise PunicaException(PunicaError.config_file_error)
    if not isinstance(deploy_information, dict):
        raise PunicaException(PunicaError.config_file_error)
    return deploy_information


def handle_invoke_config(config_dir_path: str):
    try:
        config_file_path = os.path.join(config_dir_path, 'contracts', 'test-config.json')
        with open(config_file_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise PunicaException(PunicaError.config_file_not_found)
    try:
        invoke_config = config['invokeConfig']
        password_config = config['password']
    except KeyError:
        raise PunicaException(PunicaError.config_file_error)
    if not isinstance(invoke_config, dict):
        raise PunicaException(PunicaError.config_file_error)
    return invoke_config, password_config
