from typing import List

from click import echo
from ontology.contract.neo.invoke_function import InvokeFunction
from ontology.core.invoke_transaction import InvokeTransaction

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

    def invoke(self, func: Func):
        contract_address = self.invoke_config['address']
        invoke_func = InvokeFunction(func.name, func.args_normalized)
        echo(func.name)
        echo('-' * len(func.name))
        if func.pre_exec:
            res = self.__send_tx_pre_exec(contract_address, invoke_func, func.signers)
            echo(res)
        else:
            tx_hash = self.__send_tx(contract_address, invoke_func, func.payer, func.signers)

    def __send_tx(self, contract_address: str, func: InvokeFunction, payer_address: str,
                  signer_address_list: List[str]):
        if len(payer_address) == 0:
            payer_address = self.invoke_config.get('defaultPayer', '')
        if len(payer_address) == 0:
            payer_address = input('Please input payer address: ')
        tx = self.ontology.neo_vm.make_invoke_transaction(contract_address,
                                                          func,
                                                          payer_address,
                                                          self.invoke_config.get('gasPrice', 500),
                                                          self.invoke_config.get('gasLimit', 20000))
        tx = self.__add_signature(tx, signer_address_list, payer_address)

        tx_hash = self._send_raw_tx(tx)
        self._echo_pending_tx_info(tx_hash, f'\nDeploy {contract_name}')


        tx_hash = self._send_raw_tx(tx)
        self._echo_pending_tx_info(tx_hash, f'\n{func.}')


        return self.ontology.rpc.send_raw_transaction(tx)

    def __send_tx_pre_exec(self, contract_address: str, func: InvokeFunction, signer_address_list: List[str]):
        tx = self.ontology.neo_vm.make_invoke_transaction(contract_address, func)
        tx = self.__add_signature(tx, signer_address_list)
        return self.ontology.rpc.send_raw_transaction_pre_exec(tx)

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
