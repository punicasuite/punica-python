#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from click.testing import CliRunner

from punica.cli import main


class TestScmp(unittest.TestCase):
    def test_scmp(self):
        runner = CliRunner()
        result = runner.invoke(main, ['scmp'])
        print(result)


if __name__ == '__main__':
    unittest.main()
