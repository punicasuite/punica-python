import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from punica.cli import main


class TestToolCmd(unittest.TestCase):
    @patch('getpass.getpass')
    def test_invoke_cmd(self, password):
        project_path = os.path.join(os.getcwd(), 'test_file', 'test_invoke')
        password.return_value = 'password'
        runner = CliRunner()
        result = runner.invoke(main, ['-p', '/Users/sss/dev/punicaboxdemo/initdemo', 'tool', 'transform', '--addresstohex', 'AHX1wzvdw9Yipk7E9MuLY4GGX4Ym9tHeDe'])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()