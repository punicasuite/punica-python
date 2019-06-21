import getpass

from typing import List
from getpass import getpass
from ontology.contract.neo.invoke_function import InvokeFunction

from punica.core.contract_func import Func
from punica.core.contract_project import ContractProjectWithConfig


class Invocation(ContractProjectWithConfig):
    def __init__(self, project_dir: str = '', network: str = '', wallet_path: str = '', contract_config_path: str = ''):
        super().__init__(project_dir, network, wallet_path, contract_config_path)
        invoke_config = self.contract_config.get('invoke', dict())
        if len(invoke_config) == 0:
            invoke_config = self.contract_config.get('invokeConfig', dict())
        self.__invoke_config = invoke_config

    @property
    def invoke_config(self):
        return self.__invoke_config

    def get_func_list(self) -> List[Func]:
        funcs = self.invoke_config.get('functions', list())
        for index, func in enumerate(funcs):
            funcs[index] = Func.from_dict(func)
        return funcs

    def invoke(self, func: Func):
        contract_address = self.invoke_config['address']
        invoke_func = InvokeFunction(func.name, func.args_normalized)
        if func.pre_exec:
            self.__send_tx_pre_exec(contract_address, invoke_func)
        else:
            payer_address = func.payer
            if len(payer_address) == 0:
                payer_address = self.invoke_config.get('defaultPayer', '')
            if len(payer_address) == 0:
                payer_address = input('Please input payer address: ')
            self.__send_tx(contract_address, invoke_func, payer_address)

    def __send_tx(self, contract_address: str, func: InvokeFunction, payer_address: str):
        tx = self.ontology.neo_vm.make_invoke_transaction(contract_address,
                                                          func,
                                                          payer_address,
                                                          self.invoke_config.get('gasPrice', 500),
                                                          self.invoke_config.get('gasLimit', 20000))
        password = self.contract_config.get('password', dict()).get(payer_address, '')
        if len(password) == 0:
            password = getpass(prompt=f'Unlock {payer_address}: ')
        payer = self.get_acct_by_address(payer_address, password)
        tx.sign_transaction(payer)
        return self.ontology.rpc.send_raw_transaction(tx)

    def __send_tx_pre_exec(self, contract_address: str, func: InvokeFunction):
        tx = self.ontology.neo_vm.make_invoke_transaction(contract_address, func)
        return self.ontology.rpc.send_raw_transaction_pre_exec(tx)
