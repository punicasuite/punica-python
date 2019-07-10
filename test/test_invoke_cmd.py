import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from punica.cli import main


class TestInvokeCmd(unittest.TestCase):
    def setUp(self):
        self.project_path = os.path.join(os.getcwd(), 'data', 'test_invoke')

    @patch('getpass.getpass')
    def test_invoke_cmd(self, password):
        password.return_value = 'password'
        runner = CliRunner()
        result = runner.invoke(main, ['-p', self.project_path, 'invoke'])
        print(result.output)
        self.assertEqual(0, result.exit_code)
        result = runner.invoke(main, ['-p', self.project_path, 'invoke', 'balanceOf'])
        print(result.output)


if __name__ == '__main__':
    unittest.main()
