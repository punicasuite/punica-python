#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PunicaException(Exception):
    def __init__(self, error: dict):
        super().__init__(error['code'], error['msg'])


class PunicaError:
    @staticmethod
    def get_error(code: int, msg: str) -> dict:
        error = dict()
        error['code'] = code
        error['msg'] = msg
        return error

    @staticmethod
    def other_error(msg: str) -> dict:
        if isinstance(msg, bytes):
            try:
                msg = msg.decode()
                msg = 'Other Error, ' + msg
            except UnicodeDecodeError:
                msg = 'Other Error'
        return PunicaError.get_error(59000, msg)

    invalid_box_name = get_error.__func__(10000, 'box error, invalid box name')
    config_file_not_found = get_error.__func__(10001, 'punica config file not found')
    config_file_error = get_error.__func__(10002, 'error exist in punica config file')
    wallet_file_not_found = get_error.__func__(10003, 'wallet file not found')
    wallet_file_error = get_error.__func__(10004, 'error exist in wallet file')
    wallet_file_unspecified = get_error.__func__(10005, 'please specify the wallet file you want to open')
    directory_error = get_error.__func__(10006, 'the path isn\'t a directory')
    avm_file_empty = get_error.__func__(10007, 'the avm file is empty')
    abi_file_not_found = get_error.__func__(10008, 'abi file not found')
    abi_file_empty = get_error.__func__(10009, 'abi file is empty')
    abi_file_error = get_error.__func__(10009, 'error exist in abi file')

    network_error = get_error.__func__(20000, 'please make sure you network state, and the repository exists.')

    file_exist_error = get_error.__func__(30000, 'something already exists at the destination.')
    permission_error = get_error.__func__(30001, 'permission denied, please check your file path.')
    dir_path_error = get_error.__func__(30002, 'dir path not exist, please check your dir path.')
