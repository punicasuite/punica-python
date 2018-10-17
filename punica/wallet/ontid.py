
from punica.wallet.account import Account
from punica.exception.punica_exception import PunicaException


class OntId:
    @staticmethod
    def add_ont_id(project_dir: str):
        wallet_manager = Account.get_wallet_manager(project_dir)
        try:
            pwd = Account.get_password()
            wallet_manager.create_identity('', pwd)
            wallet_manager.write_wallet()
        except PunicaException:
            pass

    @staticmethod
    def list_ont_id(project_dir: str):
        wallet_manager = Account.get_wallet_manager(project_dir)
        print('ontId:')
        for identity in wallet_manager.wallet_in_mem.identities:
            print('\t', identity.ont_id)
