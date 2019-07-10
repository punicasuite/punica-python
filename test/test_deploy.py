#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import unittest

from os import path
from ontology.utils.utils import get_random_bytes

from test import test_file_dir, ontology
from punica.deploy.deploy_contract import Deployment


class TestDeploy(unittest.TestCase):
    def setUp(self):
        self.project_path = os.path.join(test_file_dir, 'deploy', 'normalized')
        self.network = 'testNet'
        self.deployment = Deployment(self.project_path, self.network)

    def test_generate_contract_address(self):
        hex_contract_address = self.deployment.get_contract_address('oep4')
        self.assertEqual('cb9f3b7c6fb1cf2c13a40637c189bdd066a272b4', hex_contract_address)

    def test_deploy(self):
        with open(path.join(self.project_path, 'build', 'contracts', 'random.avm'), 'w') as f:
            f.write(get_random_bytes(100).hex())
        tx_hash = self.deployment.deploy_smart_contract('random')
        time.sleep(6)
        ontology.rpc.connect_to_test_net()
        deploy_information = ontology.rpc.get_transaction_by_tx_hash(tx_hash).get('Payload')
        self.assertEqual('Punica', deploy_information['Name'])
        self.assertEqual('v1.0.0', deploy_information['CodeVersion'])
        self.assertEqual('NashMiao', deploy_information['Author'])
        self.assertEqual('A contract for test Punica deploy', deploy_information['Description'])


if __name__ == '__main__':
    unittest.main()
