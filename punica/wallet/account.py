import getpass
import os

from ontology.ont_sdk import OntologySdk
from ontology.wallet.wallet_manager import WalletManager

from punica.exception.punica_exception import PunicaException, PunicaError


class Account:

    @staticmethod
    def import_account(project_path, private_key):
        wallet_path_dir = os.path.join(project_path, 'wallet')
        # TODO: the file name 'wallet.json' should be custom defined here
        wallet_path = os.path.join(wallet_path_dir, 'wallet.json')
        if not os.path.exists(wallet_path):
            os.makedirs(wallet_path_dir)
        wallet_manager = WalletManager()
        wallet_manager.open_wallet(wallet_path)
        pwd = Account.get_password()
        try:
            wallet_manager.create_account_from_private_key('', pwd, private_key)
            wallet_manager.write_wallet()
        except ValueError as e:
            print('import account error:')
            print(e.args)

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
    def delete_account(project_path, address: str):
        wallet_manager = Account.get_wallet_manager(project_path)
        for account in wallet_manager.wallet_in_mem.accounts:
            if account.get_b58_address() == address:
                pwd = getpass.getpass('Please input password: ')
                try:
                    wallet_manager.get_account(address, pwd)
                except Exception:
                    print('password is wrong')
                    return
                wallet_manager.wallet_in_mem.accounts.remove(account)
                wallet_manager.write_wallet()
                print('delete success')
                return
        print('delete failed')
        print('there is not the address: ', address)

    @staticmethod
    def list_account(project_path):
        wallet_manager = Account.get_wallet_manager(project_path)
        print('Account:')
        for account in wallet_manager.wallet_in_mem.accounts:
            print('\t{}'.format(account.get_b58_address()))

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
    def get_password():
        while True:
            acct_password = getpass.getpass('Please input password: ')
            acct_password_repeat = getpass.getpass('Please repeat password: ')
            if acct_password == acct_password_repeat:
                return acct_password
            else:
                print("password not match")
                raise PunicaException(PunicaError.other_error('password not match'))
