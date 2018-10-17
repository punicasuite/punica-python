import getpass
import os

from ontology.ont_sdk import OntologySdk
from punica.invoke.invoke_contract import Invoke

from punica.utils.handle_config import handle_network_config

from punica.wallet.account import Account
from punica.exception.punica_exception import PunicaException, PunicaError


class Asset:
    @staticmethod
    def balance_of(project_dir_path: str, asset: str, address: str, network: str):
        if asset == '' or asset.lower() != 'ont' and asset.lower() != 'ong':
            print(asset, ' asset should be ont or ong')
            return
        if project_dir_path == '':
            project_dir_path = os.getcwd()
        if not os.path.isdir(project_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        rpc_address = handle_network_config(project_dir_path, network)
        sdk = OntologySdk()
        sdk.rpc.set_address(rpc_address)
        balance = sdk.native_vm().asset().query_balance(asset, address)
        print(address + '  Balance: ', balance)

    @staticmethod
    def query_unbound_ong(project_dir_path, address, network):
        if project_dir_path == '':
            project_dir_path = os.getcwd()
        if not os.path.isdir(project_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        rpc_address = handle_network_config(project_dir_path, network)
        sdk = OntologySdk()
        sdk.rpc.set_address(rpc_address)
        balance = sdk.native_vm().asset().query_unbound_ong(address)
        print(address + '  UnboundOng: ', balance)

    @staticmethod
    def transfer(project_dir_path, asset: str, sender, to, amount, gas_price, gas_limit, network):
        if asset == '' or asset.lower() != 'ont' and asset.lower() != 'ong':
            print('asset should be ont or ong')
            return
        if project_dir_path == '':
            project_dir_path = os.getcwd()
        if not os.path.isdir(project_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        rpc_address = handle_network_config(project_dir_path, network)
        sdk = OntologySdk()
        sdk.set_rpc(rpc_address)
        wallet_manager = Account.get_wallet_manager(project_dir_path)
        if len(wallet_manager.wallet_in_mem.accounts) == 0:
            print('there is not account in the wallet.json')
            return
        has_sender = False
        for acc in wallet_manager.wallet_in_mem.accounts:
            if sender == acc.address:
                has_sender = True
                break
        if not has_sender:
            print('there is not sender in the wallet.json')
            return
        sender_account = Invoke.unlock_account(sender, wallet_manager)
        if sender_account is None:
            return
        tx_hash = sdk.native_vm().asset().send_transfer(asset, sender_account, to, amount, sender_account,
                                                        gas_limit, gas_price)
        print('tx_hash: ', tx_hash)

    @staticmethod
    def withdraw_ong(project_dir_path: str, claimer: str, to: str, amount, gas_limit, gas_price, network):
        if project_dir_path == '':
            project_dir_path = os.getcwd()
        if not os.path.isdir(project_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        rpc_address = handle_network_config(project_dir_path, network)
        sdk = OntologySdk()
        sdk.rpc.set_address(rpc_address)
        sdk.wallet_manager = Account.get_wallet_manager(project_dir_path)
        if len(sdk.wallet_manager.wallet_in_mem.accounts) == 0:
            print('there is not account in the wallet.json')
            return
        has_sender = False
        for acc in sdk.wallet_manager.wallet_in_mem.accounts:
            if claimer == acc.address:
                has_sender = True
                break
        if not has_sender:
            print('there is not sender in the wallet.json')
            return
        claimer_pwd = getpass.getpass('Please input claimer password: ')
        claimer_account = sdk.wallet_manager.get_account(claimer, claimer_pwd)
        tx_hash = sdk.native_vm().asset().send_withdraw_ong_transaction(claimer_account, to, amount, claimer_account,
                                                                        gas_limit, gas_price)
        print('tx_hash: ', tx_hash)
