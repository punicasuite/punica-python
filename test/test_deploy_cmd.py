#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from punica.cli import main

from unittest.mock import patch
from click.testing import CliRunner

from punica.compile.contract_compile import PunicaCompiler
from punica.utils.file_system import ensure_remove_dir_if_exists


class TestDeployCmd(unittest.TestCase):
    @patch('getpass.getpass')
    def test_deploy_cmd(self, password):
        project_path = os.path.join(os.path.dirname(__file__), 'test_file', 'test_deploy')
        password.return_value = 'password'
        runner = CliRunner()
        try:
            os.mkdir(project_path)
            result = runner.invoke(main, ['-p', project_path, 'init'])
            # self.assertEqual(0, result.exit_code)
            init_info = ['Downloading...', 'Unpacking...', 'Unbox successful. Enjoy it!', '']
            info_list = result.output.split('\n')
            for index, info in enumerate(info_list):
                self.assertEqual(init_info[index], info)
            result = runner.invoke(main, ['-p', project_path, 'compile'])
            print(result.output)
            # self.assertEqual(0, result.exit_code)
            info_list = result.output.split('\n')
            print(info_list)
        finally:
            ensure_remove_dir_if_exists(project_path)


if __name__ == '__main__':
    unittest.main()
