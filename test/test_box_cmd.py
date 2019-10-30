#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from click.testing import CliRunner

from punica.cli import main
from punica.utils.file_system import ensure_remove_dir_if_exists, ensure_path_exists


class TestUnbox(unittest.TestCase):
    def test_unbox(self):
        box_name = 'tutorialtoken'
        project_path = os.path.join(os.getcwd(), 'file', 'test_unbox', box_name)
        ensure_path_exists(project_path)
        try:
            runner = CliRunner()
            result = runner.invoke(main, ['unbox', '-h'])
            info_list = result.output.split('\n')
            print(info_list)
            result = runner.invoke(main, ['-p', project_path, 'unbox', box_name])
            info_list = result.output.split('\n')
            print(info_list)
        finally:
            ensure_remove_dir_if_exists(project_path)

    def test_boxes(self):
        runner = CliRunner()
        result = runner.invoke(main, ['boxes', '-h'])
        info_list = result.output.split('\n')
        print(info_list)
        result = runner.invoke(main, 'boxes')
        # info_list = result.output.split('\n')
        print(result.output)


if __name__ == '__main__':
    unittest.main()
