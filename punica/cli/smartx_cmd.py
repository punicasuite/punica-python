import webbrowser

from click import pass_context

from .main import main


@main.command('smartx')
@pass_context
def smartx_cmd(ctx):
    """
    Ontology smart contract IDE,SmartX (http://smartx.ont.io/)
    """
    webbrowser.open("https://smartx.ont.io/")
