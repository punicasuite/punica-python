#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import unittest

from unittest.mock import patch

from ontology.ont_sdk import OntologySdk

from punica.deploy.deploy_contract import Deploy


class TestDeploy(unittest.TestCase):
    def test_generate_contract_address(self):
        project_path = os.path.join(os.getcwd(), 'test_file', 'test_deploy')
        hex_contract_address = Deploy.generate_contract_address(project_path)
        self.assertEqual('f9f47e6a80482eb1c8831789f46dbc5a4f606222', hex_contract_address)

    @patch('getpass.getpass')
    def test_deploy_smart_contract(self, password):
        ontology = OntologySdk()
        rpc_address = 'http://polaris3.ont.io:20336'
        ontology.rpc.set_address(rpc_address)
        password.return_value = 'password'
        project_path = os.path.join(os.getcwd(), 'test_file', 'test_deploy')
        tx_hash = Deploy.deploy_smart_contract(project_path, 'test')
        if tx_hash is not None:
            time.sleep(6)
            deploy_information = ontology.rpc.get_raw_transaction(tx_hash)['Payload']
            self.assertEqual('Punica', deploy_information['Name'])
            self.assertEqual('1.0.0', deploy_information['CodeVersion'])
            self.assertEqual('Nash', deploy_information['Author'])
            self.assertEqual('A smart contract for test Punica deploy', deploy_information['Description'])


if __name__ == '__main__':
    unittest.main()
