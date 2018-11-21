#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from click.testing import CliRunner

from punica.cli import main


class TestUnbox(unittest.TestCase):
    def test_compile(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_cmd')
        runner = CliRunner()
        result = runner.invoke(main, ['-p', '/Users/sss/dev/localgit/ontio-community/init-advanced-box', 'compile', '--contracts', './contracts/contract_a.py'])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
