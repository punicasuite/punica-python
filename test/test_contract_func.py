import unittest

from punica.core.contract_func import Func


class TestContractFunc(unittest.TestCase):
    def test_dict(self):
        func_name = 'transferMulti'
        args = [["ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6", "ARLvwmvJ38stT9MKD78YtpDak3MENZkoxF", 1],
                ["AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve", "ARLvwmvJ38stT9MKD78YtpDak3MENZkoxF", 1]]
        payer = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6'
        signers = ["AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve", "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"]
        func = Func(func_name, args, payer, signers)
        func_dict = dict(func)
        actual = Func.from_dict(func_dict)
        self.assertEqual(func_dict, dict(actual))


if __name__ == '__main__':
    unittest.main()
