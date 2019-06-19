from click import echo
from crayons import red
from typing import Union
from ontology.utils.contract import Data
from ontology.exception.exception import SDKException

from punica.exception.punica_exception import PunicaException


def echo_cli_exception(e: Union[PunicaException, SDKException]):
    msg = e.args[1].replace('Other Error, ', '')
    if 'transactor' in msg:
        if isinstance(msg, str):
            words = msg.split(' ')
            words[0] = 'Payer'
            words[1] = Data.to_b58_address(Data.to_reserve_hex_str(words[1]))
            msg = ' '.join(words)
    echo(red(f'{msg}\n', bold=True))
