#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from punica.cli import main

from click.testing import CliRunner


class TestVersion(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def check_result(self, result):
        self.assertEqual(0, result.exit_code)
        self.assertTrue(isinstance(result.output, str))

    def test_version(self):
        result = self.runner.invoke(main, '--version')
        self.check_result(result)
        result = self.runner.invoke(main, '-v')
        self.check_result(result)


if __name__ == '__main__':
    unittest.main()
