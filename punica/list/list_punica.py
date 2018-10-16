
from punica.common.define import DEFAULT_CONFIG

from punica.utils.handle_config import handle_invoke_config


class ListPunica:
    @staticmethod
    def list_funcs(project_dir: str, config_name: str):
        if config_name == '':
            config_name = DEFAULT_CONFIG
        invoke_config, password_config = handle_invoke_config(project_dir, config_name)
        print("All Functions:")
        for function_name in invoke_config['functions'].keys():
            print('\t', function_name)



