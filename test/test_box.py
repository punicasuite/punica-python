#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from punica.box.repo_box import Box
from punica.config.punica_config import InitConfig
from punica.exception.punica_exception import PunicaException


class TestCompiler(unittest.TestCase):
    def test_init(self):
        init_to_path = os.path.join(os.getcwd(), 'init')
        Box.init_box(init_to_path)
        init_config = InitConfig(init_to_path)
        self.assertTrue(os.path.exists(init_config.src_path()))
        self.assertTrue(os.path.exists(init_config.test_path()))
        self.assertTrue(os.path.exists(init_config.wallet_path()))
        self.assertTrue(os.path.exists(init_config.contract_path()))
        self.assertTrue(os.path.exists(os.path.join(init_config.test_path(), init_config.test_template_name())))
        shutil.rmtree(init_to_path)

    def test_generate_repo_url(self):
        target_repo_url = 'https://github.com/punica-box/tutorialtoken-box.git'
        box_name = 'tutorialtoken'
        repo_url = Box.generate_repo_url(box_name)
        self.assertEqual(target_repo_url, repo_url)

    def test_git_clone(self):
        repo_to_path = os.path.join(os.getcwd(), 'test_clone')
        repo_url = 'https://github.com/wdx7266/ontology-tutorialtoken.git'
        Box.download_repo(repo_url, repo_to_path)
        try:
            shutil.rmtree(repo_to_path)
        except PermissionError:
            pass

    def test_unbox(self):
        box_name = 'tutorialtoken'
        box_to_path = os.path.join(os.getcwd(), 'test_unbox')
        try:
            Box.unbox(box_name, box_to_path)
        finally:
            shutil.rmtree(box_to_path)

        box_name = 'errorbox'
        box_to_path = os.path.join(os.getcwd(), 'test_unbox')
        try:
            Box.unbox(box_name, box_to_path)
        finally:
            shutil.rmtree(box_to_path)

    def test_list_boxes(self):
        try:
            boxes = Box.list_boxes()
            self.assertIn('interplanetary-album-box', boxes)
        except PunicaException as e:
            self.assertIn('API rate limit exceeded', e.args[1])


if __name__ == '__main__':
    unittest.main()
