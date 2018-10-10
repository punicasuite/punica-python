#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from click.testing import CliRunner

from punica.cli import main


class TestUnbox(unittest.TestCase):
    def test_unbox(self):
        box_name = 'tutorialtoken'
        unbox_to_path = os.path.join(os.getcwd(), box_name)
        try:
            os.makedirs(unbox_to_path)
        except FileExistsError:
            pass
        runner = CliRunner()
        result = runner.invoke(main, ['unbox', '-h'])
        print(result.output)
        result = runner.invoke(main, ['-p', unbox_to_path, 'unbox', 'tutorialtoken'])
        print(result)


if __name__ == '__main__':
    unittest.main()
