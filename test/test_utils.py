#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from ontology.wallet.wallet_manager import WalletManager

from punica.utils.file_system import (
    read_wallet
)

from punica.exception.punica_exception import PunicaException


class TestUtils(unittest.TestCase):
    def test_read_wallet(self):
        wallet_path = os.path.join(os.getcwd(), 'file', 'test_wallet', 'wallet')
        wallet_manager = read_wallet(wallet_path)
        self.assertTrue(isinstance(wallet_manager, WalletManager))
        wallet_manager = read_wallet(wallet_path, 'wallet.json')
        self.assertTrue(isinstance(wallet_manager, WalletManager))
        wallet_path = os.path.join(os.getcwd(), 'file', 'test_wallet', 'exist_wallet.json')
        self.assertRaises(PunicaException, read_wallet, wallet_path)
        wallet_path = os.path.join(os.getcwd(), 'file', 'test_wallet', 'error_wallet.json')
        self.assertRaises(PunicaException, read_wallet, wallet_path)


if __name__ == '__main__':
    unittest.main()
