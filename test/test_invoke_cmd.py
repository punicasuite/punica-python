import unittest

from os import path, getcwd
from unittest.mock import patch
from click.testing import CliRunner

from punica.cli import main


class TestInvokeCmd(unittest.TestCase):
    def setUp(self):
        self.project_path = path.join(getcwd(), 'file', 'invoke')
        self.runner = CliRunner()

    def test_invoke_neo_contract_cmd(self):
        self.project_path = path.join(self.project_path, 'neo', 'oep4')
        result = self.runner.invoke(main, ['-p', self.project_path, 'invoke'])
        print(result.output)
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('Invoking your contract...', info_list)
        self.assertIn('Execute NeoVm contract method init', info_list)
        self.assertIn('> Saving transaction to chain.', info_list)

    def test_invoke_neo_contract_balance_of_cmd(self):
        self.project_path = path.join(self.project_path, 'neo', 'oep4')
        result = self.runner.invoke(main, ['-p', self.project_path, 'invoke', 'balanceOf'])
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('Invoking your contract...', info_list)
        self.assertIn('Prepare execute NeoVm contract method balanceOf', info_list)

    def test_invoke_neo_contract_transfer_multi_cmd(self):
        self.project_path = path.join(self.project_path, 'neo', 'oep4')
        result = self.runner.invoke(main, ['-p', self.project_path, 'invoke', 'transferMulti'])
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('Invoking your contract...', info_list)
        self.assertIn('Execute NeoVm contract method transferMulti', info_list)

    def test_invoke_wasm_contract(self):
        self.project_path = path.join(self.project_path, 'wasm', 'basic_api')
        result = self.runner.invoke(main, ['-p', self.project_path, 'invoke', '--wasm'])
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('Invoking your contract...', info_list)
        self.assertIn('Prepare execute WebAssembly contract method add', info_list)
        self.assertIn('> result: 4', info_list)
        self.assertIn('Execute WebAssembly contract method storage_write', info_list)
        self.assertIn('> Saving transaction to chain.', info_list)
        self.assertIn('Prepare execute WebAssembly contract method storage_read', info_list)
        self.assertIn('> result: punica_cli_value', info_list)

    def test_invoke_wasm_interplanetary_album_contract(self):
        self.project_path = path.join(self.project_path, 'wasm', 'interplanetary_album')
        result = self.runner.invoke(main, ['-p', self.project_path, 'invoke', '--wasm'])
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('Invoking your contract...', info_list)
        self.assertIn('Execute WebAssembly contract method put_one_item', info_list)
        self.assertIn('> Saving transaction to chain.', info_list)
        self.assertIn('Invoking your contract...', info_list)
        self.assertIn('Prepare execute WebAssembly contract method get_item_list', info_list)
        self.assertIn('Invoking your contract...', info_list)
        self.assertIn('Execute WebAssembly contract method clear_item_list', info_list)


if __name__ == '__main__':
    unittest.main()
