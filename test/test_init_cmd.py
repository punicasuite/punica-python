#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from click.testing import CliRunner

from punica.cli import main
from punica.config.punica_config import InitConfig
from punica.utils.file_system import ensure_remove_dir_if_exists


class TestInit(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_init_empty_project(self):
        project_path = os.path.join(os.path.dirname(__file__), 'test_file', 'test_init_empty')
        try:
            result = self.runner.invoke(main, ['--project', project_path, 'init'])
            info_list = result.output.split('\n')
            init_empty_info = ['Downloading...', 'Unpacking...', 'Unbox successful. Enjoy it!']
            for index, info in enumerate(init_empty_info):
                self.assertEqual(info, info_list[index])
            self.assertEqual(0, result.exit_code)
            init_config = InitConfig(project_path)
            self.assertTrue(os.path.exists(init_config.src_path()))
            self.assertTrue(os.path.exists(init_config.test_path()))
            self.assertTrue(os.path.exists(init_config.wallet_path()))
            self.assertTrue(os.path.exists(init_config.contract_path()))
        finally:
            ensure_remove_dir_if_exists(project_path)


if __name__ == '__main__':
    unittest.main()
