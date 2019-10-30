import os
import unittest

from click.testing import CliRunner

from punica.cli import main
from punica.config.punica_config import InitConfig
from punica.utils.file_system import ensure_remove_dir_if_exists


class TestInit(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_itx_info(self):
        project_path = os.path.join(os.path.dirname(__file__), 'file', 'test_init_empty')
        try:
            result = self.runner.invoke(main, ['info','tx','3fa996e1009e1194336e1c79ca2b2cfebce37a90a4281f4068b86fbae228098b'])
            # info_list = result.output.split('\n')
            print(result.output)
        finally:
            ensure_remove_dir_if_exists(project_path)


if __name__ == '__main__':
    unittest.main()
