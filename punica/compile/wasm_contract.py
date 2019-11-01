import shutil
import subprocess
from os import path, listdir
from typing import List

from click import echo
from halo import Halo

from punica.core.base_project import BaseProject
from punica.exception.punica_exception import PunicaError, PunicaException
from punica.utils.file_system import ensure_remove_dir_if_exists, ensure_path_exists


class WasmContract(BaseProject):
    def __init__(self, project_dir: str = ''):
        super().__init__(project_dir)
        self._contract_dir = path.join(self.project_dir, 'contracts')
        self._build_release_dir = path.join(self.project_dir, 'build', 'contracts')
        self._compile_release_dir = path.join(self.contract_dir, 'target', 'wasm32-unknown-unknown', 'release')

    @property
    def contract_dir(self):
        return self._contract_dir

    @property
    def build_release_dir(self):
        return self._build_release_dir

    @property
    def compile_release_dir(self):
        return self._compile_release_dir

    @staticmethod
    def echo_compile_banner():
        msg = 'Compiling your WebAssembly contracts...'
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
            if not file.endswith('.wasm'):
                continue
            contract_list.append(file)
        return contract_list

    @staticmethod
    def run_command(cwd, command):
        proc = subprocess.Popen(command, cwd=cwd, shell=True, stdout=subprocess.PIPE)
        while True:
            line = proc.stdout.readline().rstrip()
            if not line:
                break
            yield line

    @staticmethod
    def get_all_wasm_file(dir: str) -> List[str]:
        try:
            files_in_dir = listdir(dir)
        except FileNotFoundError:
            raise PunicaException(PunicaError.pj_dir_path_error)
        contract_list = list()
        for file in files_in_dir:
            if not file.endswith('.wasm'):
                continue
            contract_list.append(file)
        return contract_list

    @staticmethod
    def is_tool_exist(name):
        return shutil.which(name) is not None

    def ensure_env_correct(self) -> bool:
        env_spinner = Halo(text=f"Checking your environment...", spinner='bouncingBar')
        env_spinner.start()
        try:
            ensure_path_exists(self.build_release_dir)
            if not self.is_tool_exist('rustup'):
                echo('Please create Rust environment first:')
                echo('1. curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly')
                echo('2. Follow the steps in https://github.com/ontio/ontology-wasm-cdt-rust')
                return False
            if not self.is_tool_exist('ontio-wasm-build'):
                echo('Please install ontology wasm contract validation and optimization tool first:')
                echo('cargo install --git=https://github.com/ontio/ontio-wasm-build')
                return False
            env_spinner.succeed()
            return True
        except Exception as e:
            env_spinner.fail()
            echo(e.args[0])
            return False

    @staticmethod
    def run_shell_command(cwd: str, cmd: str):
        proc = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE)
        try:
            proc.communicate(timeout=360)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()

    def _optimize_contract(self) -> bool:
        optimize_spinner = Halo(text=f"\nOptimizing your WebAssembly contract...", spinner='bouncingBar')
        optimize_spinner.start()
        try:
            wasm_file_list = self.get_all_wasm_file(self.compile_release_dir)
            for file in wasm_file_list:
                optimize_cmd = f'ontio-wasm-build {file} {file}'
                self.run_shell_command(self.compile_release_dir, optimize_cmd)
            optimize_spinner.succeed()
            return True
        except Exception as e:
            optimize_spinner.fail()
            echo(f'\n{e.args[0]}\n')
            return False

    def _clean_compile_env(self) -> bool:
        clean_spinner = Halo(text='Cleaning the environment...\n', spinner='bouncingBar')
        clean_spinner.start()
        try:
            wasm_file_list = self.get_all_wasm_file(self.compile_release_dir)
            for file in wasm_file_list:
                shutil.copyfile(path.join(self.compile_release_dir, file), path.join(self.build_release_dir, file))
            ensure_remove_dir_if_exists(path.join(self.contract_dir, 'target'))
            clean_spinner.succeed()
            return True
        except Exception as e:
            clean_spinner.fail()
            echo(f'\n{e.args[0]}\n')
            return False

    def compile_contract(self):
        if not self.ensure_env_correct():
            return
        compile_spinner = Halo(text=f"Compiling...", spinner='bouncingBar')
        compile_spinner.succeed()
        echo('')
        compile_cmd = 'RUSTFLAGS="-C link-arg=-zstack-size=32768" cargo build --release --target wasm32-unknown-unknown'
        self.run_shell_command(self.contract_dir, compile_cmd)
        if not self._optimize_contract():
            return
        if not self._clean_compile_env():
            return
