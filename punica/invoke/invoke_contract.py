import json

from typing import List

from halo import Halo
from click import echo
from ontology.utils.neo import NeoData
from ontology.utils.event import Event
from ontology.exception.exception import SDKException
from ontology.core.invoke_transaction import InvokeTransaction
from ontology.contract.neo.invoke_function import NeoInvokeFunction

from punica.core.contract_func import Func
from punica.core.contract_project import ContractProjectWithConfig
from punica.exception.punica_exception import PunicaException, PunicaError


class Invocation(ContractProjectWithConfig):
    def __init__(self, project_dir: str = '', network: str = '', wallet_path: str = '', contract_config_path: str = ''):
        super().__init__(project_dir, network, wallet_path, contract_config_path)
        invoke_config = self.contract_config.get('invoke', dict())
        if len(invoke_config) == 0:
            invoke_config = self.contract_config.get('invokeConfig', dict())
        self.__invoke_config = invoke_config
        self._echo_network_info()

    @property
    def invoke_config(self):
        return self.__invoke_config

    def get_func_by_name(self, func_name: str) -> Func:
        punica_func_list = self.get_func_list()
        for punica_func in punica_func_list:
            if func_name == punica_func.name:
                return punica_func
        raise PunicaException(PunicaError.invalid_contract_func_name)

    def get_func_list(self) -> List[Func]:
        func_params_list = self.invoke_config.get('functions', list())
        punica_func_list = list()
        for params in func_params_list:
            punica_func_list.append(Func.from_dict(params))
        return punica_func_list

    def invoke(self, func: Func, is_pre: bool = False):
        contract_address = self.invoke_config['address']
        if is_pre or func.pre_exec:
            self.__invoke_banner(f'Prepare execute {func.name}')
            self.__pre_invoke(contract_address, func)
        else:
            self.__invoke_banner(f'Execute {func.name}')
            self.__commit_invoke(contract_address, func)

    @staticmethod
    def __invoke_banner(msg: str):
        echo(msg)
        echo(f"{'-' * len(msg)}\n")

    def __pre_invoke(self, contract_address, func: Func):
        invoke_func = NeoInvokeFunction(func.name, func.args_normalized)
        response = self.__send_tx_pre_exec(contract_address, invoke_func, func.signers)
        self.__echo_pre_exec_result(response, func.return_type)

    @staticmethod
    def decode_raw_data(data: str, d_type: str):
        if d_type.lower() == 'hex':
            return NeoData.to_hex_str(data)
        if d_type.lower() == 'int':
            return NeoData.to_int(data)
        if d_type.lower() == 'bool':
            return NeoData.to_bool(data)
        if d_type.lower() == 'utf8':
            return NeoData.to_utf8_str(data)
        if d_type.lower() == 'dict':
            return NeoData.to_dict(data)
        if d_type.lower() == 'bytes':
            return NeoData.to_bytes(data)
        if d_type.lower() == 'address':
            return NeoData.to_b58_address(data)
        return data

    def __commit_invoke(self, contract_address: str, func: Func):
        invoke_func = NeoInvokeFunction(func.name, func.args_normalized)
        payer_address = func.payer
        if len(payer_address) == 0:
            payer_address = self.invoke_config.get('defaultPayer', '')
        if len(payer_address) == 0:
            payer_address = input('Please input payer address: ')
        tx = self.ontology.neo_vm.make_invoke_transaction(contract_address,
                                                          invoke_func,
                                                          payer_address,
                                                          self.invoke_config.get('gasPrice', 500),
                                                          self.invoke_config.get('gasLimit', 20000))
        tx = self.__add_signature(tx, func.signers, payer_address)
        tx_hash = self._send_raw_tx_with_spinner(tx)
        if len(tx_hash) != 64:
            return ''
        if self._echo_pending_tx_info(tx_hash):
            event = self.ontology.rpc.get_contract_event_by_tx_hash(tx_hash)
            notify = Event.get_notify_by_contract_address(event, contract_address)
            if len(notify) != 0:
                notify['States'] = self.parse_states(notify.get('States', dict()), func.event)
                echo('> Contract emit event:\n')
                echo('  ' + json.dumps(notify, indent=2).replace('\n', '\n  ') + '\n')
        echo(f"Using 'punica info tx {tx_hash}' to query all events in transaction.\n")
        return tx_hash

    def parse_states(self, states: List[str], states_type: List[str]):
        for i, s in enumerate(states):
            try:
                states[i] = self.decode_raw_data(s, states_type[i])
            except IndexError:
                pass
        return states

    def __echo_pre_exec_result(self, response: dict, return_type: str = ''):
        spinner = Halo(text="Parsing result...\n", spinner='dots')
        spinner.start()
        if not isinstance(response, dict):
            spinner.fail()
            return
        try:
            response['Result'] = self.decode_raw_data(response.get('Result', ''), return_type)
            spinner.succeed()
        except SDKException as e:
            spinner.fail()
            echo(f'\n{e.args[1]}\n')
        echo("")
        echo(f"> gas:    {response.get('Gas', '')}")
        echo(f"> state:  {response.get('State', '')}")
        echo(f"> result: {response.get('Result', '')}")
        echo(f"> notify: {response.get('Notify', list())}\n")

    def __send_tx_pre_exec(self, contract_address: str, func: NeoInvokeFunction, signer_address_list: List[str]):
        tx = self.ontology.neo_vm.make_invoke_transaction(contract_address, func)
        tx = self.__add_signature(tx, signer_address_list)
        res = self._send_raw_tx_pre_exec_with_spinner(tx)
        return res

    def __add_signature(self, tx: InvokeTransaction, signer_address_list: List[str], payer_address: str = ''):
        if len(payer_address) == 34:
            payer = self.get_acct_by_address(payer_address)
            tx.sign_transaction(payer)
        for signer_address in signer_address_list:
            if signer_address == payer_address:
                continue
            signer = self.get_acct_by_address(signer_address)
            tx.add_sign_transaction(signer)
        return tx
