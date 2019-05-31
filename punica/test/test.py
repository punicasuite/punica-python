import os

from punica.invoke.invoke_contract import Invoke

from punica.utils.file_system import read_abi


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
