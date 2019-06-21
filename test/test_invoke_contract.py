#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from unittest.mock import patch

from punica.invoke.invoke_contract import Invocation


class TestUtils(unittest.TestCase):
    @patch('getpass.getpass')
    def test_invoke_all_function_in_list(self, password):
        network = 'privateNet'
        wallet_file_name = 'wallet.json'
        password.return_value = 'password'
        project_path = os.path.join(os.getcwd(), 'test_file', 'test_invoke')
        Invocation.invoke_all_function_in_list(wallet_file_name, project_path, network, 'Name,BalanceOf')


if __name__ == '__main__':
    unittest.main()
