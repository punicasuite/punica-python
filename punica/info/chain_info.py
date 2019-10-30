import json

from click import echo
from ontology.sdk import Ontology

from punica.core.project_with_config import ProjectWithConfig


class Info(ProjectWithConfig):
    def __init__(self, project_dir: str = '', network: str = ''):
        super().__init__(project_dir)
        if len(network) == 0:
            network = self.default_network
        self._ontology = Ontology()
        self._ontology.rpc.set_address(self.get_rpc_address(network))

    @property
    def ontology(self):
        return self._ontology

    @staticmethod
    def echo_dict_info(info: dict):
        echo(json.dumps(info, indent=2))


class AccountInfo(Info):
    def __init__(self, project_dir: str = '', network: str = ''):
        super().__init__(project_dir, network)

    def query_balance(self, b58_address: str):
        balance = self.ontology.rpc.get_balance(b58_address)
        self.echo_dict_info(balance)


class BlockInfo(Info):
    def __init__(self, project_dir: str = '', network: str = ''):
        super().__init__(project_dir, network)

    def query_block(self, tx_hash: str):
        block_info = self.ontology.rpc.get_block_by_hash(tx_hash)
        self.echo_dict_info(block_info)


class ContractInfo(Info):
    def __init__(self, project_dir: str = '', network: str = ''):
        super().__init__(project_dir, network)

    def query_contract(self, hex_contract_address: str):
        contract_info = self.ontology.rpc.get_contract(hex_contract_address)
        self.echo_dict_info(contract_info)


class TxInfo(Info):
    def __init__(self, project_dir: str = '', network: str = ''):
        super().__init__(project_dir, network)

    def query_event(self, tx_hash: str):
        event = self.ontology.rpc.get_contract_event_by_tx_hash(tx_hash)
        self.echo_dict_info(event)
