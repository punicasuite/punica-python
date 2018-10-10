#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from click.testing import CliRunner

from punica.cli import main


class TestUnbox(unittest.TestCase):
    def test_compile(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_cmd', 'oep4.py')
        runner = CliRunner()
        result = runner.invoke(main, ['compile', contract_path])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
