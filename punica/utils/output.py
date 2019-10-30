from click import echo
from crayons import red
from typing import Union
from ontology.utils.neo import NeoData
from ontology.exception.exception import SDKException

from punica.exception.punica_exception import PunicaException


def echo_cli_exception(e: Union[PunicaException, SDKException]):
    msg = e.args[1].replace('Other Error, ', '')
    if 'transactor' in msg:
        if isinstance(msg, str):
            words = msg.split(' ')
            words[0] = 'Payer'
            words[1] = NeoData.to_b58_address(NeoData.to_reserve_hex_str(words[1]))
            msg = ' '.join(words)
    echo(red(f'\n{msg}\n', bold=True))
