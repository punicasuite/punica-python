from click import (
    argument,
    pass_context,
)

from punica.info.chain_info import (
    TxInfo,
    AccountInfo,
    ContractInfo
)

from .main import main


@main.group('info')
@pass_context
def info_cmd(ctx):
    """
    Display information in the blockchain.
    """
    pass


@info_cmd.command('tx')
@argument('tx_hash', nargs=1, default="")
@pass_context
def tx_info_cmd(ctx, tx_hash: str):
    """
    Display transaction information.
    """
    tx_info = TxInfo(ctx.obj['PROJECT_DIR'])
    tx_info.query_event(tx_hash)


@info_cmd.command('contract')
@argument('contract_address', nargs=1)
@pass_context
def contract_info_cmd(ctx, contract_address: str):
    """
    Display contract information.
    """
    contract_info = ContractInfo(ctx.obj['PROJECT_DIR'])
    contract_info.query_contract(contract_address)


@info_cmd.command('balance')
@argument('address', nargs=1)
@pass_context
def balance_info_cmd(ctx, address: str):
    """
    Display account balance information.
    """
    account_info = AccountInfo(ctx.obj['PROJECT_DIR'])
    account_info.query_balance(address)
