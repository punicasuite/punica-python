#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from click.testing import CliRunner

from punica.cli import main


class TestUnbox(unittest.TestCase):
    def test_unbox(self):
        runner = CliRunner()
        result = runner.invoke(main, ['-h'])
        print(result.output)
        result = runner.invoke(main, ['-v'])
        print(result.output)


if __name__ == '__main__':
    unittest.main()
