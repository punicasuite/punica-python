import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from punica.cli import main


class TestListCmd(unittest.TestCase):
    @patch('getpass.getpass')
    def test_list_cmd(self, password):
        project_path = os.path.join(os.getcwd(), 'data', 'test_list')
        password.return_value = 'password'
        runner = CliRunner()
        result = runner.invoke(main, ['-p', project_path, 'list'])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()