import json
import time

from os import path
from click import echo
from ontology.exception.exception import SDKException
from ontology.sdk import Ontology

from punica.core.project import Project
from punica.exception.punica_exception import PunicaException, PunicaError


class ContractProject(Project):
    def __init__(self, project_dir: str = '', network: str = '', wallet_path: str = '', contract_config_path: str = ''):
        super().__init__(project_dir)
        if len(contract_config_path) == 0:
            contract_config_path = path.join(self.project_dir, 'contracts', 'config.json')
        try:
            with open(contract_config_path, 'r') as f:
                self._contract_config = json.load(f)
        except FileNotFoundError:
            raise PunicaException(PunicaError.config_file_not_found)
        self._avm_dir = path.join(project_dir, 'build', 'contracts')
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
        echo(f'> Gas price:    {self.ontology.rpc.get_gas_price()}\n\n')

    def _echo_tx_info(self, tx_hash: str, title: str = '') -> bool:
        tx_info = dict()
        for _ in range(5):
            try:
                time.sleep(6)
                tx_info = self.ontology.rpc.get_transaction_by_tx_hash(tx_hash)
                break
            except SDKException:
                continue
        if len(tx_info) == 0:
            return False
        payer = tx_info.get('Payer', '')
        balance = self.ontology.rpc.get_balance(payer)
        if len(title) != 0:
            echo(''.join([title, '\n', len(title) * '-']))
        echo(f'> transaction hash:    {tx_hash}')
        echo(f"> block height:        {tx_info.get('Height', '')}")
        echo(f"> nonce:               {tx_info.get('Nonce', '')}")
        echo(f"> gas price:           {tx_info.get('GasPrice', '')}")
        echo(f"> gas limit:           {tx_info.get('GasLimit', '')}")
        echo(f"> payer:               {payer}")
        echo(f"> balance:             {balance['ONT']} ONT, {balance['ONG'] * (10 ** -9)} ONG\n")
        echo('> Saving transaction to chain.\n')
        return True

    def get_acct_by_address(self, address: str, password: str):
        return self.ontology.wallet_manager.get_account_by_b58_address(address, password)
