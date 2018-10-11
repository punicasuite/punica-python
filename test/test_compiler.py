#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from punica.compile.contract_compile import PunicaCompiler


class TestCompiler(unittest.TestCase):
    def test_compile_contract_remote(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'oep4.py')
        PunicaCompiler.compile_contract(contract_path)
        avm_save_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'oep4.avm')
        abi_save_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'oep4_abi.json')
        avm_local_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'oep4.avm')
        abi_local_path = os.path.join(os.getcwd(), 'test_file', 'test_compile_remote', 'oep4_abi.json')
        with open(avm_save_path, 'r') as f:
            avm_save = f.read()
        with open(avm_local_path, 'r') as f2:
            avm_local = f2.read()
            self.assertEqual(avm_save, avm_local)
        with open(abi_save_path, 'r') as f3:
            abi_save = f3.read()
        with open(abi_local_path, 'r') as f4:
            abi_local = f4.read()
            self.assertEqual(abi_save, abi_local)
        os.remove(avm_save_path)
        os.remove(abi_save_path)

    def test_compile_contract(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'contracts', 'oep4.py')
        PunicaCompiler.compile_contract(contract_path)
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
        PunicaCompiler.generate_avm_file(contract_path)
        split_path = os.path.split(contract_path)
        save_path = os.path.join(os.getcwd(), 'build', split_path[1])
        avm_save_path = save_path.replace('.py', '.avm')
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

    def test_generate_abi_file(self):
        contract_path = os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.py')
        PunicaCompiler.generate_abi_file(contract_path)
        split_path = os.path.split(contract_path)
        save_path = os.path.join(os.getcwd(), 'build', split_path[1])
        abi_save_path = save_path.replace('.py', '.json')
        with open(os.path.join(os.getcwd(), 'test_file', 'test_compile', 'oep4.json'), 'r') as f:
            target_abi = f.read()
        with open(abi_save_path, 'r') as f:
            abi = f.read()
            self.assertEqual(target_abi, abi)
        os.remove(abi_save_path)
        os.removedirs('build')


if __name__ == '__main__':
    unittest.main()
