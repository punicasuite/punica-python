import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from punica.cli import main


class TestToolCmd(unittest.TestCase):
    @patch('getpass.getpass')
    def test_invoke_cmd(self, password):
        password.return_value = 'password'
        runner = CliRunner()
        result = runner.invoke(main, ['tool', 'transform'])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
