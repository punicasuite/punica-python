#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from ontology.wallet.wallet_manager import WalletManager

from punica.utils.file_system import (
    read_avm,
    read_wallet
)

from punica.utils.cli_config import (
    handle_network_config,
    handle_deploy_config
)

from punica.exception.punica_exception import PunicaException


class TestUtils(unittest.TestCase):
    def test_read_wallet(self):
        wallet_path = os.path.join(os.getcwd(), 'test_file', 'test_wallet', 'wallet')
        wallet_manager = read_wallet(wallet_path)
        self.assertTrue(isinstance(wallet_manager, WalletManager))
        wallet_manager = read_wallet(wallet_path, 'wallet.json')
        self.assertTrue(isinstance(wallet_manager, WalletManager))
        wallet_path = os.path.join(os.getcwd(), 'test_file', 'test_wallet', 'exist_wallet.json')
        self.assertRaises(PunicaException, read_wallet, wallet_path)
        wallet_path = os.path.join(os.getcwd(), 'test_file', 'test_wallet', 'error_wallet.json')
        self.assertRaises(PunicaException, read_wallet, wallet_path)

    def test_handle_network_config(self):
        config_dir_path = os.path.join(os.getcwd(), 'test_file', 'test_config')
        rpc_address = handle_network_config(config_dir_path)
        self.assertEqual('http://127.0.0.1:7545', rpc_address)
        rpc_address = handle_network_config(config_dir_path, 'test')
        self.assertEqual('http://polaris3.ont.io:20336', rpc_address)
        self.assertRaises(PunicaException, handle_network_config, config_dir_path, 'testNet')
        config_dir_path = os.getcwd()
        self.assertRaises(PunicaException, handle_network_config, config_dir_path)

    def test_handle_deploy_information_config(self):
        config_dir_path = os.path.join(os.getcwd(), 'test_file', 'test_config')
        deploy_information = handle_deploy_config(config_dir_path)
        self.assertIn('name', deploy_information)
        self.assertIn('desc', deploy_information)
        self.assertIn('email', deploy_information)
        self.assertIn('author', deploy_information)
        self.assertIn('version', deploy_information)
        self.assertRaises(PunicaException, handle_deploy_config, os.getcwd())

    def test_read_avm(self):
        avm_dir_path = os.path.join(os.getcwd(), 'test_file', 'test_file_system')
        hex_avm_code = read_avm(avm_dir_path)
        self.assertEqual(5278, len(hex_avm_code))
        self.assertTrue(isinstance(hex_avm_code, str))


if __name__ == '__main__':
    unittest.main()
