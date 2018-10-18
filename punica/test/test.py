import json
import os

from punica.utils.handle_config import handle_invoke_config

from punica.common.define import DEFAULT_CONFIG

from punica.exception.punica_exception import PunicaException, PunicaError


class Test:
    @staticmethod
    def generate_test_template(project_dir_path, config, abi):
        if project_dir_path == '':
            project_dir_path = os.getcwd()
        if not os.path.isdir(project_dir_path):
            raise PunicaException(PunicaError.dir_path_error)
        if abi != '':
            abi_path = os.path.join(project_dir_path, abi)
            if not os.path.exists(abi_path):
                abi_path = os.path.join(project_dir_path, 'contracts', 'build', abi)
                if not os.path.exists(abi_path):
                    print(abi_path, 'not exist')
                    os._exit(0)
            Test.generate_test_file(project_dir_path, '',abi_path)
        else:
            if config != '':
                config_path = os.path.join(project_dir_path, config)
                if not os.path.exists(config):
                    config_path = os.path.join(project_dir_path, 'contracts', config)
            else:
                config_path = os.path.join(project_dir_path, 'contracts', DEFAULT_CONFIG)
                if not os.path.exists(config_path):
                    print(config_path, 'not exist')
                    os._exit(0)
            invoke_dict, password = handle_invoke_config(project_dir_path, os.path.basename(config_path))
            abi_path = os.path.join(project_dir_path, 'contracts', 'build', invoke_dict['abi'])
            if not os.path.exists(abi_path):
                print(abi_path, 'not exist')
                os._exit(0)
            Test.generate_test_file(project_dir_path, abi_path)

    @staticmethod
    def generate_test_file(project_dir_path, abi_path):
        with open(abi_path, 'r') as f:
            dict_abi = json.loads(f.read())
            functions = dict_abi['functions']
            abi_name = os.path.basename(abi_path)
            class_name = abi_name.split('_')[0]
            class_name.capitalize()
            test_dir_path = os.path.join(project_dir_path, 'test')
            test_file_path = os.path.join(test_dir_path, 'test_' + class_name +'.py')
            print('generating test file')
            if not os.path.exists(test_dir_path):
                os.makedirs(test_dir_path)
            with open(test_file_path, 'w') as f:
                f.writelines('import json' + '\n')
                f.writelines('import unittest' + '\n')
                f.writelines('from punica.invoke.invoke_contract import Invoke' + '\n')
                f.writelines('from ontology.ont_sdk import OntologySdk' + '\n')
                f.writelines('from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo' + '\n')
                f.writelines('\n')
                f.writelines('sdk = OntologySdk()' + '\n')
                f.writelines('sdk.set_rpc()' + '\n')
                f.writelines('contract_address = \'\'' + '\n')
                f.writelines('wallet_path=\'\'' + '\n')
                f.writelines('sdk.wallet_manager.open_wallet(wallet_path)' + '\n')
                f.writelines('acct = sdk.wallet_manager.get_account(\'\', \'\')' + '\n')
                f.writelines('payer = sdk.wallet_manager.get_account(\'\', \'\')' + '\n')
                f.writelines('gas_limit = 20000' + '\n')
                f.writelines('gas_price = 500' + '\n')
                f.writelines('abi_path = \'\'' + '\n')
                f.writelines('with open(abi_path, 'r') as f:' + '\n')
                f.writelines('    dict_abi = json.loads(f.read())' + '\n')
                f.writelines('    functions = dict_abi[\'functions\']' + '\n')
                f.writelines('abi_info = AbiInfo(dict_abi[\'hash\'], dict_abi[\'entrypoint\'], dict_abi[\'functions\'], dict_abi[\'events\'])' + '\n')
                f.writelines('\n')
                f.writelines('class Test'+ class_name +'(unittest.TestCase):' + '\n')
                for func in functions:
                    f.writelines('   '+'def ' + 'test_' + func['name'].lower()+'(self):' + '\n')
                    f.writelines('            pre_exec = True' + '\n')
                    f.writelines('            function_name = \'\'' + '\n')
                    f.writelines('            params = dict()' + '\n')
                    f.writelines('            params[\'\'] = \'\'' + '\n')
                    f.writelines('            abi_function = Invoke.get_function(params, function_name, abi_info)' + '\n')
                    f.writelines('            sdk.neo_vm().send_transaction(contract_address, acct, payer, gas_limit, gas_price, abi_function, pre_exec)' + '\n')
                f.writelines('if __name__ == \'__main__\':' + '\n')
                f.writelines('      ' + 'unittest.main()' + '\n')
            print('test file in :')
            print(test_file_path)
            print('complete , enjoy it')






