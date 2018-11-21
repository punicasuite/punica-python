from Cryptodome import Random
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.crypto.signature_scheme import SignatureScheme


class Tool:
    @staticmethod
    def address_to_hex(address):
        if address is None or address == '':
            print('address is none')
            return
        print('Result is:')
        print('\t', Address.b58decode(address).to_array().hex())

    @staticmethod
    def str_to_hex(any_str: str):
        print('Result is:')
        print('\t', any_str.encode().hex())

    @staticmethod
    def hex_reverse(any_hex: str):
        res = bytearray.fromhex(any_hex)
        res.reverse()
        print('Result is:')
        print('\t', res.hex())

    @staticmethod
    def num_to_hex(num: int):
        print('Result is:')
        print('\t', hex(num))

    @staticmethod
    def generate_random_private_key():
        private_key = Random.get_random_bytes(64).hex()[:64]
        print('Result is:')
        print('\t', private_key)

    @staticmethod
    def decrypt_private_key(key, address, salt, n, password):
        if n == 0:
            n = 16384
        private_key = Account.get_gcm_decoded_private_key(key, password, address, salt, n, SignatureScheme.SHA256withECDSA)
        print('Result is:')
        print('\t', private_key)