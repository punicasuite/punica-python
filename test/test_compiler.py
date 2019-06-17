#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from punica.compile import py_contract


class TestCompiler(unittest.TestCase):

    def test_compile_contract_remote(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'oep4.py')
        py_contract.compile_contract(contract_path)
        avm_save_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'build', 'oep4.avm')
        abi_save_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'build', 'oep4_abi.json')
        with open(avm_save_path, 'r') as f:
            avm_save = f.read()
            self.assertIsNotNone(avm_save)
        with open(abi_save_path, 'r') as f3:
            abi_save = f3.read()
            self.assertIsNotNone(abi_save)
        os.remove(avm_save_path)
        os.remove(abi_save_path)

    def test_compile_contract(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'contracts', 'oep4.py')
        py_contract.compile_contract(contract_path)
        split_path = os.path.split(contract_path)
        save_path = os.path.join(os.getcwd(), 'build', split_path[1])
        avm_save_path = save_path.replace('.py', '.avm')
        abi_save_path = save_path.replace('.py', '.json')
        with open(os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.avm'), 'r') as f:
            target_avm = f.read()
        with open(os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.json'), 'r') as f:
            target_abi = f.read()
        with open(avm_save_path, 'r') as f:
            hex_avm_code = f.read()
            self.assertEqual(target_avm, hex_avm_code)
        with open(abi_save_path, 'r') as f:
            abi = f.read()
            self.assertEqual(target_abi, abi)
        os.remove(avm_save_path)
        os.remove(abi_save_path)
        os.removedirs('build')

    def test_generate_avm_file(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.py')
        split_path = os.path.split(contract_path)
        save_path = os.path.join(os.getcwd(), 'build', split_path[1])
        avm_save_path = save_path.replace('.py', '.avm')
        py_contract.compile_py_contract_in_local(contract_path, avm_save_path)
        with open(os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.avm'), 'r') as f:
            target_avm = f.read()
        with open(avm_save_path, 'r') as f:
            hex_avm_code = f.read()
            self.assertEqual(target_avm, hex_avm_code)
        os.remove(avm_save_path)
        os.removedirs('build')

    def test_generate_avm_code(self):
        path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.py')
        hex_avm = PunicaCompiler.generate_avm_code(path)
        with open(os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.avm'), 'r') as f:
            self.assertEqual(f.read(), hex_avm)

    def test_generate_invoke_config(self):
        abi_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4_token_abi.json')
        invoke_config_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'invoke_config.json')
        PunicaCompiler.generate_invoke_config(abi_path, invoke_config_path)
        os.remove(invoke_config_path)

    def test_update_invoke_config(self):
        abi_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4_token_abi.json')
        invoke_config_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'invoke_config.json')
        PunicaCompiler.update_invoke_config(abi_path, invoke_config_path)
        os.remove(invoke_config_path)


if __name__ == '__main__':
    unittest.main()
