import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from punica.cli import main


class TestAccountCmd(unittest.TestCase):
    @patch('getpass.getpass')
    def test_account_cmd(self, password):
        project_path = os.path.join(os.getcwd(), 'test_file', 'test_account')
        password.return_value = 'password'
        runner = CliRunner()
        result = runner.invoke(main, ['-p', project_path, 'account', '--i', '1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114'])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()