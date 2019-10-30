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
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('This contract exist in current network.', info_list)

    @patch('getpass.getpass')
    def test_deploy_wasm_contract_cmd(self, password):
        self.project_path = path.join(self.project_path, 'wasm', 'oep4')
        password.return_value = global_wallet_password
        result = self.runner.invoke(main, ['-p', self.project_path, 'deploy', '--wasm', '--wallet', global_wallet_path])
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('This contract exist in current network.', info_list)


if __name__ == '__main__':
    unittest.main()
