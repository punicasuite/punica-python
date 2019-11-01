import json
import urllib3
import requests

from halo import Halo
from click import echo
from typing import List
from crayons import red
from os import path, listdir

from punica.core.base_project import BaseProject
from punica.exception.punica_exception import PunicaException, PunicaError

from punica.utils.file_system import (
    ensure_file_exists,
    save_avm_file
)


class PyContract(BaseProject):
    def __init__(self, project_dir: str = ''):
        super().__init__(project_dir)
        self._contract_dir = path.join(self.project_dir, 'contracts')
        self.v2_prefix = "OntCversion = '2.0.0'"
        self.v1_py_contract_compile_url = "https://smartxcompiler1.ont.io/api/v1.0/python/compile"
        self.v2_py_contract_compile_url = "https://smartxcompiler1.ont.io/api/v2.0/python/compile"
        self.csharp_contract_compile_url = "https://smartxcompiler1.ont.io/api/v1.0/csharp/compile"

    @property
    def contract_dir(self):
        return self._contract_dir

    @staticmethod
    def echo_compile_banner():
        msg = 'Compiling your NeoVm contracts...'
        echo(f'\n{msg}')
        msg = len(msg) * '='
        echo(f'{msg}\n')

    def get_all_contract(self) -> List[str]:
        try:
            files_in_dir = listdir(self.contract_dir)
        except FileNotFoundError:
            raise PunicaException(PunicaError.pj_dir_path_error)
        contract_list = list()
        for file in files_in_dir:
            if not file.endswith('.py'):
                continue
            contract_list.append(file)
        return contract_list

    def get_contract_path(self, contract_name: str):
        contract_path = path.join(self.project_dir, 'contracts', contract_name)
        if not path.exists(contract_path):
            return ''
        return contract_path

    def get_avm_save_path(self, contract_name: str):
        avm_save_path = path.join(self.project_dir, 'build', 'contracts', contract_name)
        if not avm_save_path.endswith('.py'):
            return ''
        avm_save_path = avm_save_path.replace('.py', '.avm')
        return avm_save_path

    def prepare_to_compile(self, contract_name: str):
        prepare_spinner = Halo(text="Preparing to compile", spinner='dots')
        prepare_spinner.start()
        contract_path = self.get_contract_path(contract_name)
        if len(contract_path) == 0:
            prepare_spinner.fail()
            echo(f'Contract {contract_name} not exist.')
            return '', ''
        avm_save_path = self.get_avm_save_path(contract_name)
        if len(avm_save_path) == 0:
            prepare_spinner.fail()
            echo('Punica is currently supporting contract in Python.')
            return '', ''
        ensure_file_exists(avm_save_path)
        prepare_spinner.succeed()
        return contract_path, avm_save_path

    def compile_contract(self, contract_name: str, is_v1: bool = False):
        title = contract_name.replace('.py', '')
        echo(title)
        echo('-' * len(title))
        contract_path, avm_save_path = self.prepare_to_compile(contract_name)
        compile_spinner = Halo(text=f"Compiling {contract_name}", spinner='bouncingBar')
        compile_spinner.start()
        try:
            avm_code, err_info = self.compile_py_contract_in_remote(contract_path, is_v1)
        except requests.exceptions.RequestException as e:
            compile_spinner.fail()
            while not isinstance(e, str):
                e = e.args[0]
            e = e.replace(': ', ':\n')
            echo(f'\n{e}\n')
            return False
        if len(avm_code) == 0:
            compile_spinner.fail()
            if len(err_info) == 0:
                err_info = 'An error occur in remote server.'
            echo(red(f'\n{err_info}\n', bold=True))
            return False
        compile_spinner.succeed()
        save_spinner = Halo(text=f'Saving avm file...')
        save_spinner.start()
        try:
            save_avm_file(avm_code, avm_save_path)
        except PunicaException as e:
            save_spinner.fail()
            echo(e.args[1])
            return False
        save_spinner.succeed()
        end_msg = f'> Avm file written to {path.split(avm_save_path)[0]}'
        echo(''.join(['-' * len(end_msg)]))
        echo(f'{end_msg}\n')
        return True

    def compile_py_contract_in_remote(self, contract_path: str, is_v1: bool = False) -> (str, str):
        payload = self.generate_compile_payload(contract_path)
        url = self.get_compiler_url(contract_path, is_v1)
        urllib3.disable_warnings()
        res = requests.post(url, json=payload, headers={'Content-type': 'application/json'}, timeout=10, verify=False)
        result = json.loads(res.content)
        if result["errcode"] != 0:
            return '', result.get('errdetail', '')
        return result.get('avm', ''), ''

    @staticmethod
    def generate_compile_payload(contract_path: str):
        payload = dict(type='Python')
        with open(contract_path, 'r') as f:
            payload['code'] = f.read()
        return payload

    def is_v2_py_contract(self, contract_code: str):
        return True if self.v2_prefix in contract_code[:30] else False

    def get_compiler_url(self, contract_file_name: str, is_v1: bool = False):
        if contract_file_name.endswith('.py'):
            if is_v1:
                return self.v1_py_contract_compile_url
            else:
                return self.v2_py_contract_compile_url
        return self.csharp_contract_compile_url
