#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from click.testing import CliRunner

from punica.cli import main
from punica.config.punica_config import InitConfig


class TestInit(unittest.TestCase):
    def test_initializing_empty_project(self):
        init_to_path = os.path.join(os.getcwd(), 'init_to_path')
        try:
            os.makedirs(init_to_path)
        except FileExistsError:
            pass
        runner = CliRunner()
        result = runner.invoke(main, ['-p', init_to_path, 'init'])
        self.assertEqual(0, result.exit_code)
        init_config = InitConfig(init_to_path)
        self.assertTrue(os.path.exists(init_config.src_path()))
        self.assertTrue(os.path.exists(init_config.test_path()))
        self.assertTrue(os.path.exists(init_config.wallet_path()))
        self.assertTrue(os.path.exists(init_config.contract_path()))
        shutil.rmtree(init_to_path)


if __name__ == '__main__':
    unittest.main()
