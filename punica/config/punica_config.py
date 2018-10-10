#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class InitConfig:
    def __init__(self, repo_path: str):
        self.__path = repo_path

    def contract_path(self) -> str:
        contract_path = os.path.join(self.__path, 'contracts')
        return contract_path

    @staticmethod
    def test_template_name() -> str:
        file_name = 'test_template.py'
        return file_name

    def src_path(self) -> str:
        src_path = os.path.join(self.__path, 'src')
        return src_path

    def test_path(self) -> str:
        test_path = os.path.join(self.__path, 'test')
        return test_path

    def wallet_path(self) -> str:
        wallet_path = os.path.join(self.__path, 'wallet')
        return wallet_path
