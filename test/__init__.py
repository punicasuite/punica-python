from os import path, environ, getcwd
from subprocess import Popen, PIPE

from ontology.sdk import Ontology

global_wallet_password = environ['PUNICA_CLI_PASSWORD']
global_wallet_path = path.join(path.dirname(__file__), 'wallet.json')
test_file_dir = path.join(getcwd(), 'file')
ontology = Ontology()
