import os

from punica.utils.handle_config import handle_invoke_config


class ListPunica:
    @staticmethod
    def list_funcs(project_dir: str, config_name: str):
        config_dir = os.path.join(project_dir, 'contracts')
        if config_name == '':
            config_dir = os.path.join(config_dir, 'default-config.json')
        else:
            config_dir = os.path.join(config_dir, config_name)
        if not os.path.exists(config_dir):
            print(config_dir, " not exist")
        else:
            invoke_config, password_config = handle_invoke_config(project_dir, 'default-config.json')
            print("All Functions:")
            for function_name in invoke_config['functions'].keys():
                print('\t', function_name)



