#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import unittest
from os import path

from unittest.mock import patch

from ontology.utils.utils import get_random_bytes

from test import wallet_password, test_file_dir, ontology
from punica.deploy.deploy_contract import Deployment


class TestDeploy(unittest.TestCase):
    def setUp(self):
        self.project_path = os.path.join(test_file_dir, 'test_deploy')
        self.network = 'testNet'

    def test_generate_contract_address(self):
        hex_contract_address = Deployment.generate_contract_address(self.project_path)
        self.assertEqual('3310277e27a0ed749a3525ca2f898ebcd7d6631e', hex_contract_address)

    @patch('getpass.getpass')
    def test_unnormalized_deploy_contract(self, password):
        project_path = os.path.join(self.project_path, 'unnormalized')
        tx_hash = Deployment.deploy_smart_contract(project_path, self.network)
        password.return_value = wallet_password
        print(tx_hash)

    @patch('getpass.getpass')
    def test_normalized_deploy_contract(self, password):
        project_path = os.path.join(self.project_path, 'normalized')
        tx_hash = Deployment.deploy_smart_contract(project_path, self.network)
        self.assertEqual(0, len(tx_hash))
        password.return_value = wallet_password
        with open(path.join(project_path, 'contracts', 'build', 'random.avm'), 'w') as f:
            f.write(get_random_bytes(100).hex())
        tx_hash = Deployment.deploy_smart_contract(project_path, self.network, 'random.avm')
        time.sleep(6)
        ontology.rpc.connect_to_test_net()
        deploy_information = ontology.rpc.get_transaction_by_tx_hash(tx_hash).get('Payload')
        self.assertEqual('Punica', deploy_information['Name'])
        self.assertEqual('1.0.0', deploy_information['CodeVersion'])
        self.assertEqual('NashMiao', deploy_information['Author'])
        self.assertEqual('A contract for test Punica deploy', deploy_information['Description'])


if __name__ == '__main__':
    unittest.main()
