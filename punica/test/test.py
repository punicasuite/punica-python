import json
import os

from punica.invoke.invoke_contract import Invoke

from punica.utils.file_system import read_abi

from punica.utils.handle_config import handle_invoke_config

from punica.common.define import DEFAULT_CONFIG

from punica.exception.punica_exception import PunicaException, PunicaError


class Test:
    @staticmethod
    def get_abi_info(abi_dir_path: str):
        abi_dict = read_abi(abi_dir_path, os.path.basename(abi_dir_path))
        return Invoke.generate_abi_info(abi_dict)

    @staticmethod
    def test_file(project_dir_path, file_name):
        if file_name != '':
            test_file_path = os.path.join(project_dir_path, file_name)
            if not os.path.exists(test_file_path):
                test_file_path = os.path.join(project_dir_path, 'test', file_name)
                if not os.path.exists(test_file_path):
                    print(test_file_path, 'not exist')
                    os._exit(0)
            file_name = os.path.basename(test_file_path)
            if not file_name.endswith('.py'):
                print('file type is wrong')
                os._exit(0)
            os.system('python ' + test_file_path)
        else:
            test_file_dir = os.path.join(project_dir_path, 'test')
            if not os.path.exists(test_file_dir):
                print(test_file_dir, 'not exist')
                os._exit(0)
            file_list = os.listdir(test_file_dir)
            if len(file_list) == 0:
                print(test_file_dir, 'is nil')
            for f in file_list:
                file_name = os.path.basename(f)
                if file_name.endswith('.py'):
                    os.system('python ' + os.path.join('test', f))

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
            class_name = abi_name.replace('_abi.json', '')
            test_dir_path = os.path.join(project_dir_path, 'test')
            test_file_path = os.path.join(test_dir_path, 'test_' + class_name +'.py')
            if os.path.exists(test_file_path):
                test_file_path = os.path.join(test_dir_path, 'test_' + class_name + str(2) + '.py')
            if not os.path.exists(test_dir_path):
                os.makedirs(test_dir_path)
            with open(test_file_path, 'w') as f:
                f.writelines('import unittest' + '\n')
                f.writelines('from punica.invoke.invoke_contract import Invoke' + '\n')
                f.writelines('from ontology.ont_sdk import OntologySdk' + '\n')
                f.writelines('from punica.test.test import Test' + '\n')
                f.writelines('\n')
                f.writelines('gas_limit = 20000' + '\n')
                f.writelines('gas_price = 500' + '\n')
                f.writelines(
                    'abi_path = ' + '\'' + os.path.join('contracts', 'build', os.path.basename(abi_path)) + '\'' + '\n')
                f.writelines('contract_address = ' + '\'' + dict_abi['hash'].replace('0x', '') + '\'' + '\n')
                f.writelines('wallet_path= ' + '\'' + 'wallet/wallet.json' + '\'' + '\n')
                f.writelines('\n')
                f.writelines('sdk = OntologySdk()' + '\n')
                f.writelines('sdk.set_rpc'+'(' + '\'' + 'http://polaris1.ont.io' + '\'' + ')' + '\n')
                f.writelines('sdk.wallet_manager.open_wallet(wallet_path)' + '\n')
                f.writelines('acct = sdk.wallet_manager.get_account(\'\', \'\')' + ' # input account address from wallet and password' +'\n')
                f.writelines('payer = sdk.wallet_manager.get_account(\'\', \'\')' + ' # input account address from wallet and password' + '\n')
                f.writelines('abi_info = Test.get_abi_info(abi_path)' + '\n')
                f.writelines('\n')
                f.writelines('\n')
                class_name = class_name.capitalize()
                f.writelines('class Test' + class_name +'(unittest.TestCase):' + '\n')
                for func in functions:
                    f.writelines('\n')
                    f.writelines('   '+'def ' + 'test_' + func['name'].lower()+'(self):' + '\n')
                    f.writelines('            pre_exec = True' + '\n')
                    f.writelines('            params = dict()' + '\n')
                    for param in func['parameters']:
                        f.writelines('            params'+ '['+ '\'' +param['name'] + '\''+ ']'+ '='+ '\'\'' + '\n')
                    f.writelines('            abi_function = Invoke.get_function(params, '+ '\''+func['name'] + '\'' +', abi_info)' + '\n')
                    f.writelines('            response = sdk.neo_vm().send_transaction(contract_address, acct, payer, gas_limit, gas_price, abi_function, pre_exec)' + '\n')
                    f.writelines('            print(response)' + '\n')
                f.writelines('\n')
                f.writelines('if __name__ == \'__main__\':' + '\n')
                f.writelines('      ' + 'unittest.main()' + '\n')
            print('generated test file in :')
            print(test_file_path)






