import time
import crayons

from click import echo
from getpass import getpass
from os import path, listdir

from halo import Halo
from ontology.exception.exception import SDKException

from punica.core.contract_project import ContractProjectWithConfig
from punica.exception.punica_exception import PunicaException, PunicaError


class Deployment(ContractProjectWithConfig):
    def __init__(self, project_dir: str = '', network: str = '', wallet_path: str = '', contract_config_path: str = ''):
        super().__init__(project_dir, network, wallet_path, contract_config_path)
        self._avm_dir = path.join(self.project_dir, 'build', 'contracts')

    @property
    def avm_dir(self):
        return self._avm_dir

    def __echo_contract_info(self, file_name: str, contract_deploy_info: dict, ending_msg: str = ''):
        banner = file_name.replace('.avm', '')
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
            echo(crayons.red(f'{ending_msg}\n', bold=True))

    def get_all_avm_file(self):
        try:
            files_in_dir = listdir(self.avm_dir)
        except FileNotFoundError:
            raise PunicaException(PunicaError.pj_dir_path_error)
        avm_file_list = list()
        for file in files_in_dir:
            if not file.endswith('.avm'):
                continue
            avm_file_list.append(file)
        return avm_file_list

    def deploy_smart_contract(self, contract_name: str) -> str:
        self._echo_network_info()
        try:
            hex_contract_address = self.get_contract_address(contract_name)
        except PunicaException:
            echo(crayons.red('No avm file found in this project, please compile first.\n', bold=True))
            return ''
        try:
            contract = self.ontology.rpc.get_contract(hex_contract_address)
            self.__echo_contract_info(contract_name, contract, 'This contract exist in current network.')
            return ''
        except SDKException as e:
            if 'unknow contract' not in e.args[1] and 'unknown contract' not in e.args[1]:
                raise e
        contract_config = self.contract_config
        try:
            deploy_config = contract_config['deploy']
        except KeyError:
            echo(crayons.red('Please provide deployment config.\n', bold=True))
            return ''
        payer_address = deploy_config.get('payer', '')
        if len(payer_address) == 0:
            payer_address = input('Please input payer address: ')
        password = contract_config.get('password', dict()).get(payer_address, '')
        if len(password) == 0:
            password = getpass(prompt='Please input payer account password: ')
        payer = self.get_acct_by_address(payer_address, password)
        avm_code = self.get_avm_code(contract_name)
        if len(avm_code) == 0:
            return ''
        tx = self.ontology.neo_vm.make_deploy_transaction(
            avm_code,
            deploy_config.get('needStorage', True),
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
        tx_hash = self.ontology.rpc.send_raw_transaction(tx)
        echo('Deployment transaction has been send into network...\n')

        spinner = Halo(text="Checking transaction status...\n", spinner='dots')
        spinner.start()
        tx_info = dict()
        for _ in range(5):
            try:
                time.sleep(6)
                tx_info = self.ontology.rpc.get_transaction_by_tx_hash(tx_hash)
                break
            except SDKException:
                continue
        if len(tx_info) == 0:
            spinner.fail()
            echo(f"Using 'punica info status {tx_hash}' to query transaction status.")
            return ''
        spinner.succeed()
        self._echo_tx_info(tx_hash, f'\nDeploy {contract_name}')
        return tx_hash

    def get_avm_file_path(self, file_name: str):
        if not file_name.endswith('.avm'):
            file_name = ''.join([file_name, '.avm'])
        avm_file_path = path.join(self.avm_dir, file_name)
        if not path.exists(avm_file_path):
            raise PunicaException(PunicaError.avm_file_not_found)
        return avm_file_path

    def get_avm_code(self, file_name: str):
        avm_file_path = self.get_avm_file_path(file_name)
        with open(avm_file_path, 'r') as f:
            avm_code = f.read()
        if len(avm_code) == 0:
            echo(crayons.red('No avm code found in file', bold=True))
            return ''
        return avm_code

    def get_contract_address(self, file_name: str) -> str:
        avm_code = self.get_avm_code(file_name)
        contract_address = self.ontology.neo_vm.address_from_avm_code(avm_code)
        return contract_address.hex()
