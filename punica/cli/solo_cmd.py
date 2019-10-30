import webbrowser

from click import pass_context

from .main import main


@main.command('solo')
@pass_context
def solo_chain_cmd(ctx):
    """
    One-click personal blockchain for Ontology development.
    """
    webbrowser.open('https://github.com/punicasuite/solo-chain/releases')
