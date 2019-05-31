#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from click.testing import CliRunner

from punica.cli import main
from punica.utils.file_system import ensure_remove_dir_if_exists


class TestCompileCmd(unittest.TestCase):
    def test_compile(self):
        project_path = os.path.join(os.path.dirname(__file__), 'test_file', 'test_compile_init_box')
        runner = CliRunner()
        try:
            os.mkdir(project_path)
            result = runner.invoke(main, ['-p', project_path, 'init'])
            self.assertEqual(0, result.exit_code)
            init_info = ['Downloading...', 'Unpacking...', 'Unbox successful. Enjoy it!']
            info_list = result.output.split('\n')
            for index, info in enumerate(init_info):
                self.assertEqual(info, info_list[index])
            result = runner.invoke(main, ['-p', project_path, 'compile'])
            self.assertEqual(0, result.exit_code)
            compile_info = ['Compiling...', 'Compile hello_ontology.py', 'Compiled, Thank you',
                            'Generate avm file successful...']
            info_list = result.output.split('\n')
            for index, info in enumerate(compile_info):
                self.assertEqual(info, info_list[index])
        finally:
            ensure_remove_dir_if_exists(project_path)


if __name__ == '__main__':
    unittest.main()
