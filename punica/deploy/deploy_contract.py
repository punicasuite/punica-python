from os import path, listdir

import crayons
from click import echo
from ontology.contract.wasm.vm import WasmVm
from ontology.exception.exception import SDKException

from punica.core.contract_project import ContractProjectWithConfig
from punica.exception.punica_exception import PunicaException, PunicaError


class Deployment(ContractProjectWithConfig):
    def __init__(self, project_dir: str = '', network: str = '', wallet_path: str = '', contract_config_path: str = ''):
        super().__init__(project_dir, network, wallet_path, contract_config_path)
        self._contract_build_dir = path.join(self.project_dir, 'build', 'contracts')

    @property
    def contract_build_dir(self):
        return self._contract_build_dir

    def __echo_contract_info(self, file_name: str, contract_deploy_info: dict, ending_msg: str = '',
                             ending_msg_is_red: bool = True):
        file_name = file_name.replace('.wasm', '')
        file_name = file_name.replace('.avm', '')
        banner = f'The {file_name} contract info in blockchain'
        echo(banner)
        echo('-' * len(banner))
        address = self.ontology.neo_vm.address_from_avm_code(contract_deploy_info.get('Code', ''))
        echo(f"> contract address: {address.hex()}")
        echo(f"> name:             {contract_deploy_info.get('Name', '')}")
        echo(f"> email:            {contract_deploy_info.get('Email', '')}")
        echo(f"> author:           {contract_deploy_info.get('Author', '')}")
        echo(f"> version:          {contract_deploy_info.get('CodeVersion', '')}")
        echo(f"> description:      {contract_deploy_info.get('Description', '')}")
        if len(ending_msg) != 0:
            echo(''.join(['-' * len(ending_msg)]))
            if ending_msg_is_red:
                echo(crayons.red(f'{ending_msg}\n', bold=True))
                return
            echo(f'{ending_msg}\n')

    def get_all_wasm_file(self):
        try:
            files_in_dir = listdir(self.contract_build_dir)
        except FileNotFoundError:
            raise PunicaException(PunicaError.pj_dir_path_error)
        avm_file_list = list()
        for file in files_in_dir:
            if not file.endswith('.wasm'):
                continue
            avm_file_list.append(file)
        return avm_file_list

    def get_all_avm_file(self):
        try:
            files_in_dir = listdir(self.contract_build_dir)
        except FileNotFoundError:
            raise PunicaException(PunicaError.pj_dir_path_error)
        avm_file_list = list()
        for file in files_in_dir:
            if not file.endswith('.avm'):
                continue
            avm_file_list.append(file)
        return avm_file_list

    def deploy_wasm_contract(self, contract_name: str) -> str:
        self._echo_network_info()
        try:
            hex_contract_address = self.get_wasm_contract_address(contract_name)
        except PunicaException:
            echo(crayons.red('No wasm file found in this project, please compile first.\n', bold=True))
            return ''
        except SDKException:
            echo(crayons.red('Invalid wasm file found in this project.\n', bold=True))
            return ''
        if self.is_contract_in_network(contract_name, hex_contract_address):
            return ''
        deploy_config = self.get_deploy_config()
        payer_address = self.get_payer_address()
        payer = self.get_acct_by_address(payer_address)
        wasm_code = self.get_wasm_code(contract_name)
        if len(wasm_code) == 0:
            return ''
        tx = self.ontology.wasm_vm.make_deploy_transaction(
            wasm_code,
            deploy_config.get('name', ''),
            deploy_config.get('version', ''),
            deploy_config.get('author', ''),
            deploy_config.get('email', ''),
            deploy_config.get('desc', ''),
            deploy_config.get('gasPrice', 500),
            deploy_config.get('gasLimit', 20000000),
            payer_address
        )
        tx.sign_transaction(payer)
        tx_hash = self._send_raw_tx_with_spinner(tx)
        if len(tx_hash) != 64:
            return ''
        if self._echo_pending_tx_info(tx_hash, f'\nDeploy {contract_name}'):
            contract = self.ontology.rpc.get_contract(hex_contract_address)
            self.__echo_contract_info(contract_name, contract,
                                      'You can invoke your WebAssembly contract by contract address.',
                                      ending_msg_is_red=False)
        return tx_hash

    def deploy_neo_contract(self, contract_name: str) -> str:
        self._echo_network_info()
        try:
            hex_contract_address = self.get_neo_contract_address(contract_name)
        except PunicaException:
            echo(crayons.red('No avm file found in this project, please compile first.\n', bold=True))
            return ''
        except SDKException:
            echo(crayons.red('Invalid avm file found in this project.\n', bold=True))
            return ''
        if self.is_contract_in_network(contract_name, hex_contract_address):
            return ''
        deploy_config = self.get_deploy_config()
        payer_address = self.get_payer_address()
        payer = self.get_acct_by_address(payer_address)
        avm_code = self.get_avm_code(contract_name)
        if len(avm_code) == 0:
            return ''
        tx = self.ontology.neo_vm.make_deploy_transaction(
            avm_code,
            deploy_config.get('name', ''),
            deploy_config.get('version', ''),
            deploy_config.get('author', ''),
            deploy_config.get('email', ''),
            deploy_config.get('desc', ''),
            deploy_config.get('gasPrice', 500),
            deploy_config.get('gasLimit', 20000000),
            payer_address
        )
        tx.sign_transaction(payer)
        tx_hash = self._send_raw_tx_with_spinner(tx)
        if len(tx_hash) != 64:
            return ''
        if self._echo_pending_tx_info(tx_hash, f'\nDeploy {contract_name}'):
            contract = self.ontology.rpc.get_contract(hex_contract_address)
            self.__echo_contract_info(contract_name, contract,
                                      'You can invoke your NeoVm contract by contract address.',
                                      ending_msg_is_red=False)
        return tx_hash

    def is_contract_in_network(self, contract_name: str, contract_address: str) -> bool:
        try:
            contract = self.ontology.rpc.get_contract(contract_address)
            self.__echo_contract_info(contract_name, contract, 'This contract exist in current network.')
            return True
        except SDKException as e:
            msg = str(e.args[1]).lower()
            if 'unknow contract' not in msg or 'unknown contract' not in msg:
                return False
            raise e

    def get_deploy_config(self) -> dict:
        try:
            return self.contract_config['deploy']
        except KeyError:
            echo(crayons.red('Please provide deployment config.\n', bold=True))
            raise PunicaException(PunicaError.config_file_error)

    def get_payer_address(self):
        deploy_config = self.get_deploy_config()
        payer_address = deploy_config.get('payer', '')
        if len(payer_address) == 0:
            payer_address = input('Please input payer address: ')
        while len(payer_address) != 34:
            payer_address = input('Invalid payer address, please input payer address again: ')
        return payer_address

    def get_avm_file_path(self, file_name: str):
        if not file_name.endswith('.avm'):
            file_name = ''.join([file_name, '.avm'])
        avm_file_path = path.join(self.contract_build_dir, file_name)
        if not path.exists(avm_file_path):
            raise PunicaException(PunicaError.avm_file_not_found)
        return avm_file_path

    def get_wasm_file_path(self, file_name: str):
        if not file_name.endswith('.wasm'):
            file_name = ''.join([file_name, '.wasm'])
        wasm_file_path = path.join(self.contract_build_dir, file_name)
        if not path.exists(wasm_file_path):
            raise PunicaException(PunicaError.wasm_file_not_found)
        return wasm_file_path

    def get_avm_code(self, file_name: str) -> str:
        avm_file_path = self.get_avm_file_path(file_name)
        with open(avm_file_path, 'r') as f:
            avm_code = f.read()
        if len(avm_code) == 0:
            echo(crayons.red('No avm code found in file', bold=True))
            return ''
        return avm_code

    def get_wasm_code(self, file_name: str) -> str:
        wasm_file_path = self.get_wasm_file_path(file_name)
        return WasmVm.open_wasm(wasm_file_path)

    def get_neo_contract_address(self, file_name: str) -> str:
        avm_code = self.get_avm_code(file_name)
        contract_address = self.ontology.neo_vm.address_from_avm_code(avm_code)
        return contract_address.hex()

    def get_wasm_contract_address(self, file_name: str) -> str:
        wasm_code = self.get_wasm_code(file_name)
        contract_address = self.ontology.wasm_vm.address_from_wasm_code(wasm_code)
        return contract_address.hex()
