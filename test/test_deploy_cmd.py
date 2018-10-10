#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from unittest.mock import patch

from click.testing import CliRunner

from punica.cli import main


class TestDeployCmd(unittest.TestCase):
    @patch('getpass.getpass')
    def test_deploy_cmd(self, password):
        project_path = os.path.join(os.getcwd(), 'test_file', 'test_deploy')
        password.return_value = 'password'
        runner = CliRunner()
        result = runner.invoke(main, ['-p', project_path, 'deploy', '--avm', 'oep4.avm'])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
