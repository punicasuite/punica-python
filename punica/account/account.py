import getpass
import os

from ontology.ont_sdk import OntologySdk


class Account:
    @staticmethod
    def execute(project_path: str, add, l, delete: str, i: str):
        wallet_path_dir = os.path.join(project_path, 'wallet')
        wallet_path = os.path.join(wallet_path_dir, 'wallet.json')
        if not os.path.exists(wallet_path):
            os.makedirs(wallet_path_dir)
        sdk = OntologySdk()
        sdk.wallet_manager.open_wallet(wallet_path)
        if isinstance(add, tuple):
            try:
                pwd = Account.get_password()
                sdk.wallet_manager.create_account('', pwd)
                sdk.wallet_manager.write_wallet()
            except RuntimeError as e:
                pass
        elif delete != '':
            pass
        elif i != '':
            pwd = Account.get_password()
            try:
                sdk.wallet_manager.create_account_from_private_key('', pwd, i)
                sdk.wallet_manager.write_wallet()
            except ValueError as e:
                print('import account error:')
                print(e.args)
        elif isinstance(l, tuple):
            accounts = sdk.wallet_manager.wallet_in_mem.accounts
            print('Account:')
            for account in accounts:
                print('\t{}'.format(account.address))
        else:
            print('unsupported operator')

    @staticmethod
    def get_password():
        print('\tCreate account:')
        while True:
            acct_password = getpass.getpass('\tPlease input account password: ')
            acct_password_repeat = getpass.getpass('\tPlease repeat account password: ')
            if acct_password == acct_password_repeat:
                return acct_password
            else:
                print("password not match")
                raise RuntimeError("password not match")
            print('\tCreate account successful...')





