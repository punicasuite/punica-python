import webbrowser

from click import pass_context

from .main import main


@main.command('smartx')
@pass_context
def smartx_cmd(ctx):
    """
    One-stop IDE for smart contract.
    """
    webbrowser.open("https://smartx.ont.io/")
