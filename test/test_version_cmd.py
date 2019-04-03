#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from click.testing import CliRunner

from punica.cli import main


class TestVersion(unittest.TestCase):
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(main, ['-v'])
        self.assertEqual(0, result.exit_code)
        self.assertTrue(isinstance(result.output, str))


if __name__ == '__main__':
    unittest.main()
