import os
import unittest
from os import path
from unittest import mock

from click.testing import CliRunner

from punica.cli import main
from punica.utils.file_system import ensure_remove_dir_if_exists


class TestCompileCmd(unittest.TestCase):
    def setUp(self):
        self.project_path = path.join(path.dirname(__file__), 'file', 'compile')
        self.runner = CliRunner()

    def tearDown(self):
        ensure_remove_dir_if_exists(path.join(self.project_path, 'build'))

    def test_compile_neo_py_contract(self):
        self.project_path = path.join(self.project_path, 'neo', 'oep4')
        result = self.runner.invoke(main, ['-p', self.project_path, 'compile'])
        self.assertEqual(0, result.exit_code)
        info_list = result.output.split('\n')
        self.assertIn('Compiling your NeoVm contracts...', info_list)
        self.assertIn('oep4', info_list)

    def test_compile_wasm_rust_contract(self):
        self.project_path = path.join(self.project_path, 'wasm', 'hello_world')
        result = self.runner.invoke(main, ['-p', self.project_path, 'compile', '--wasm'])
        # self.assertEqual(0, result.exit_code)
        print(result.output)


if __name__ == '__main__':
    unittest.main()
