import unittest

from punica.cli import main

from click.testing import CliRunner


class TestHelpCmd(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_help_cmd(self):
        result = self.runner.invoke(main, '--help')
        self.assertEqual(0, result.exit_code)
        print(result.output)

    def test_compile_help_cmd(self):
        result = self.runner.invoke(main, ['compile', '--help'])
        self.assertEqual(0, result.exit_code)
        print(result.output)


if __name__ == '__main__':
    unittest.main()
