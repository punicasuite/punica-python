import json
import time

from os import path
from click import echo
from getpass import getpass

from halo import Halo
from crayons import red
from ontology.sdk import Ontology
from ontology.account.account import Account
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException

from punica.core.project_with_config import ProjectWithConfig
from punica.exception.punica_exception import PunicaException, PunicaError


class ContractProjectWithConfig(ProjectWithConfig):
    def __init__(self, project_dir: str = '', network: str = '', wallet_path: str = '', contract_config_path: str = ''):
        super().__init__(project_dir)
        contract_config_file_path = path.join(self.project_dir, 'contracts', 'config.json')
        old_contract_config_file_path = path.join(self.project_dir, 'contracts', 'default-config.json')
        if len(contract_config_path) != 0:
            self._contract_config_file_path = contract_config_path
        elif path.exists(contract_config_file_path):
            self._contract_config_file_path = contract_config_file_path
        elif path.exists(old_contract_config_file_path):
            self._contract_config_file_path = old_contract_config_file_path
        else:
            raise PunicaException(PunicaError.config_file_not_found)
        try:
            with open(self._contract_config_file_path, 'r') as f:
                self._contract_config = json.load(f)
        except FileNotFoundError:
            raise PunicaException(PunicaError.config_file_not_found)
        self._contract_build_dir = path.join(project_dir, 'build', 'build')
        self._wallet_dir = path.join(project_dir, 'wallet')
        if len(network) == 0:
            network = self.default_network
        self._network = network
        self._ontology = Ontology()
        self._ontology.rpc.set_address(self.get_rpc_address(network))
        if len(wallet_path) == 0:
            wallet_path = path.join(self.wallet_dir, self._contract_config.get('defaultWallet', 'wallet.json'))
        self._wallet_path = wallet_path
        self._ontology.wallet_manager.open_wallet(self._wallet_path)

    @property
    def ontology(self):
        return self._ontology

    @property
    def network(self):
        return self._network

    @property
    def wallet_dir(self):
        return self._wallet_dir

    @property
    def contract_config(self):
        return self._contract_config

    def _echo_network_info(self):
        echo(f'> Network name: {self.network}')
        echo(f'> Network id:   {self.ontology.rpc.get_network_id()}')
        echo(f'> Gas price:    {self.ontology.rpc.get_gas_price()}\n')

    def _send_raw_tx_with_spinner(self, tx: Transaction) -> str:
        spinner = Halo(text="Sending transaction into network...\n", spinner='dots')
        msg = ''
        for _ in range(5):
            try:
                time.sleep(1)
                tx_hash = self.ontology.rpc.send_raw_transaction(tx)
                spinner.succeed()
                return tx_hash
            except SDKException as e:
                msg = str(e.args[1]).replace('Other Error, ', '')
                continue
        spinner.fail()
        echo(red(f'\n{msg}\n', bold=True))
        return ''

    def _send_raw_tx_pre_exec_with_spinner(self, tx: Transaction) -> dict:
        spinner = Halo(text="Sending transaction into network...\n", spinner='dots')
        res = dict()
        msg = ''
        for _ in range(5):
            try:
                time.sleep(1)
                res = self.ontology.rpc.send_raw_transaction_pre_exec(tx)
                spinner.succeed()
                break
            except SDKException as e:
                msg = str(e.args[1]).replace('Other Error, ', '')
                continue
        if len(res) == 0:
            spinner.fail()
            echo(red(f'\n{msg}\n', bold=True))
        return res

    def _echo_pending_tx_info(self, tx_hash: str, title: str = '') -> bool:
        spinner = Halo(text="Checking transaction status...", spinner='dots')
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
            return False
        spinner.succeed()
        payer = tx_info.get('Payer', '')
        balance = self.ontology.rpc.get_balance(payer)
        echo('')
        if len(title) != 0:
            echo(title)
            echo('-' * len(title))
        echo(f'> transaction hash:    {tx_hash}')
        echo(f"> block height:        {tx_info.get('Height', '')}")
        echo(f"> nonce:               {tx_info.get('Nonce', '')}")
        echo(f"> gas price:           {tx_info.get('GasPrice', '')}")
        echo(f"> gas limit:           {tx_info.get('GasLimit', '')}")
        echo(f"> payer:               {payer}")
        echo(f"> balance:             {balance['ONT']} ONT, {balance['ONG'] * (10 ** -9)} ONG\n")
        echo('> Saving transaction to chain.\n')
        return True

    def get_acct_by_address(self, address: str) -> Account:
        password = self.contract_config.get('password', dict()).get(address, '')
        while len(password) == 0:
            password = getpass(prompt=f'Unlock {address}: ')
        while True:
            try:
                return self.ontology.wallet_manager.get_account_by_b58_address(address, password)
            except SDKException as e:
                if 100017 == e.args[0]:
                    password = getpass(prompt=f'Password error, try again: ')
                    continue
                else:
                    raise PunicaException(PunicaError.config_file_error)
