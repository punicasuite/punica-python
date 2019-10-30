"""
Copyright (C) 2018-2019 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

from os import path
from unittest.mock import patch
from click.testing import CliRunner

from punica.cli import main

from test import global_wallet_path, global_wallet_password


class TestDeployCmd(unittest.TestCase):
    def setUp(self):
        self.project_path = path.join(path.dirname(__file__), 'file', 'deploy')
        self.runner = CliRunner()

    @patch('getpass.getpass')
    def test_deploy_neo_contract_cmd(self, password):
        self.project_path = path.join(self.project_path, 'neo', 'oep4')
        password.return_value = global_wallet_password
        result = self.runner.invoke(main, ['-p', self.project_path, 'deploy', '--wallet', global_wallet_path])
        info_list = result.output.split('\n')
        self.assertIn('This contract exist in current network.', info_list)

    @patch('getpass.getpass')
    def test_deploy_wasm_contract_cmd(self, password):
        self.project_path = path.join(self.project_path, 'wasm', 'oep4')
        password.return_value = global_wallet_password
        result = self.runner.invoke(main, ['-p', self.project_path, 'deploy', '--wasm', '--wallet', global_wallet_path])
        info_list = result.output.split('\n')
        self.assertIn('This contract exist in current network.', info_list)


if __name__ == '__main__':
    unittest.main()
