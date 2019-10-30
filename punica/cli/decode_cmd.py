from click import (
    argument,
    pass_context,
    echo
)

from ontology.core.transaction import Transaction
from ontology.utils import utils
from ontology.utils.neo import NeoData

from punica.cli import main
from punica.info.chain_info import Info


@main.group('decode')
@pass_context
def decode_cmd(ctx):
    """
    Decode Hex string to readable values.
    """
    pass


@decode_cmd.command('tx')
@argument('raw_tx', nargs=1, default="")
@pass_context
def to_tx_cmd(ctx, raw_tx: str):
    """
    Decode HEX string to transaction information.
    """
    tx = Transaction.deserialize_from(utils.hex_to_bytes(raw_tx))
    Info.echo_dict_info(dict(tx))


@decode_cmd.command('bool')
@argument('file', nargs=1, default="")
@pass_context
def to_bool_cmd(ctx, data: str):
    """
    Decode Hex string to bool.
    """
    echo(NeoData.to_bool(data))


@decode_cmd.command('utf8')
@argument('file', nargs=1, default="")
@pass_context
def to_utf8_cmd(ctx, data: str):
    """
    Decode Hex string to UTF-8 string.
    """
    echo(NeoData.to_utf8_str(data))


@decode_cmd.command('address')
@argument('file', nargs=1, default="")
@pass_context
def to_b58_address_cmd(ctx, data: str):
    """
    Decode Hex string to Base58 encode string.
    """
    echo(NeoData.to_b58_address(data))


@decode_cmd.command('dict')
@argument('file', nargs=1, default="")
@pass_context
def to_dict_cmd(ctx, data: str):
    """
    Decode Hex string to JSON string.
    """
    Info.echo_dict_info(NeoData.to_dict(data))


@decode_cmd.command('hex')
@argument('file', nargs=1, default="")
@pass_context
def to_hex_cmd(ctx, data: str):
    """
    Convert ASCII string to a HEX string.
    """
    echo(NeoData.to_hex_str(data))


@decode_cmd.command('int')
@argument('file', nargs=1, default="")
@pass_context
def to_int_cmd(ctx, data: str):
    """
    Convert ASCII string to a number.
    """
    echo(NeoData.to_int(data))
