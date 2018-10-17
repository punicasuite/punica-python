import getpass
import os

from ontology.ont_sdk import OntologySdk
from ontology.wallet.wallet_manager import WalletManager

from punica.exception.punica_exception import PunicaException, PunicaError


class Account:

    @staticmethod
    def get_wallet_manager(project_path: str):
        wallet_path_dir = os.path.join(project_path, 'wallet')
        wallet_path = os.path.join(wallet_path_dir, 'wallet.json')
        if not os.path.exists(wallet_path):
            os.makedirs(wallet_path_dir)
        wallet_manager = WalletManager()
        wallet_manager.open_wallet(wallet_path)
        return wallet_manager

    @staticmethod
    def list_account(project_path):
        wallet_manager = Account.get_wallet_manager(project_path)
        print('Account:')
        for account in wallet_manager.wallet_in_mem.accounts:
            print('\t{}'.format(account.address))

    @staticmethod
    def add_account(project_path):
        wallet_manager = Account.get_wallet_manager(project_path)
        try:
            print('Create account:')
            pwd = Account.get_password()
            wallet_manager.create_account('', pwd)
            wallet_manager.write_wallet()
        except RuntimeError as e:
            print('write wallet file error')
            print(e.args)
        except PunicaException:
            pass

    @staticmethod
    def execute(project_path: str, delete: str, i: str):
        wallet_path_dir = os.path.join(project_path, 'wallet')
        wallet_path = os.path.join(wallet_path_dir, 'wallet.json')
        if not os.path.exists(wallet_path):
            os.makedirs(wallet_path_dir)
        sdk = OntologySdk()
        sdk.wallet_manager.open_wallet(wallet_path)
        if delete != '':
            pass
        elif i != '':
            pwd = Account.get_password()
            try:
                sdk.wallet_manager.create_account_from_private_key('', pwd, i)
                sdk.wallet_manager.write_wallet()
            except ValueError as e:
                print('import account error:')
                print(e.args)
        else:
            print('unsupported operator')

    @staticmethod
    def get_password():
        while True:
            acct_password = getpass.getpass('Please input password: ')
            acct_password_repeat = getpass.getpass('Please repeat password: ')
            if acct_password == acct_password_repeat:
                return acct_password
            else:
                print("password not match")
                raise PunicaException(PunicaError.other_error('password not match'))





