#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json

from git import RemoteProgress, Repo, GitCommandError
import click
import requests
from halo import Halo

from punica.utils.file_system import (
    ensure_remove_dir_if_exists,
    remove_file_if_exists,
    ensure_path_exists
)

from punica.exception.punica_exception import PunicaError, PunicaException


class Box:
    @staticmethod
    def handle_ignorance(repo_to_path: str = ''):
        spinner = Halo(text="Unpacking...", spinner='dots')
        spinner.start()
        box_ignore_file_path = os.path.join(repo_to_path, 'punica-box.json')
        try:
            with open(box_ignore_file_path, 'r') as f:
                box_ignore_files = json.load(f)['ignore']
        except FileNotFoundError:
            spinner.succeed()
            return
        remove_file_if_exists(box_ignore_file_path)
        for file in box_ignore_files:
            try:
                file_path = os.path.join(repo_to_path, file)
                ensure_remove_dir_if_exists(file_path)
                remove_file_if_exists(file_path)
            except (PermissionError, FileNotFoundError):
                pass
        spinner.succeed()

    @staticmethod
    def git_clone(repo_url: str, repo_to_path: str = ''):
        if repo_to_path == '':
            repo_to_path = os.getcwd()
        if os.listdir(repo_to_path):
            raise PunicaException(PunicaError.file_exist_error)
        download_spinner = Halo(text="Downloading...", spinner='dots')
        receiving_spinner = Halo(spinner='dots')
        resolving_spinner = Halo(spinner='dots')
        counting_spinner = Halo(spinner='dots')
        compressing_spinner = Halo(spinner='dots')

        spinners = [download_spinner, receiving_spinner, resolving_spinner, counting_spinner, compressing_spinner]

        def update(self, op_code, cur_count, max_count=None, message=''):
            if download_spinner.spinner_id is not None and len(download_spinner.text) != 0:
                download_spinner.succeed()
            if op_code == RemoteProgress.COUNTING:
                if counting_spinner.spinner_id is None:
                    counting_spinner.start()
                scale = round(cur_count / max_count * 100, 2)
                counting_spinner.text = f'Counting objects: {scale}% ({cur_count}/{max_count})'
                if scale == 100:
                    counting_spinner.succeed()
            if op_code == RemoteProgress.COMPRESSING:
                if compressing_spinner.spinner_id is None:
                    compressing_spinner.start()
                scale = round(cur_count / max_count * 100, 2)
                compressing_spinner.text = f'Compressing objects: {scale}% ({cur_count}/{max_count})'
                if scale == 100:
                    compressing_spinner.succeed()
            if op_code == RemoteProgress.RECEIVING:
                if receiving_spinner.spinner_id is None:
                    receiving_spinner.start()
                scale = round(cur_count / max_count * 100, 2)
                receiving_spinner.text = f'Receiving objects: {scale}%, {message}'
                if scale == 100:
                    receiving_spinner.succeed()
            if op_code == RemoteProgress.RESOLVING:
                if resolving_spinner.spinner_id is None:
                    resolving_spinner.start()
                scale = round(cur_count / max_count * 100, 2)
                resolving_spinner.text = f'Resolving deltas: {scale}%'
                if scale == 100:
                    resolving_spinner.succeed()

        RemoteProgress.update = update

        try:
            download_spinner.start()
            Repo.clone_from(url=repo_url, to_path=repo_to_path, depth=1, progress=RemoteProgress())
            for spinner in spinners:
                if spinner.spinner_id is not None and len(spinner.text) != 0:
                    spinner.fail()
        except GitCommandError as e:
            download_spinner.fail()
            network_error = 'Could not read from remote repository'
            file_exist_error = 'already exists and is not an empty directory'
            if network_error in str(e.args[2]):
                raise PunicaException(PunicaError.network_error)
            elif file_exist_error in str(e.args[2]):
                raise PunicaException(PunicaError.file_exist_error)
            else:
                raise PunicaException(PunicaError.other_error(e.args[2]))

    @staticmethod
    def init(init_to_path: str):
        if init_to_path == '':
            init_to_path = os.getcwd()
        ensure_path_exists(init_to_path)
        repo_url = 'https://github.com/punica-box/punica-init-default-box'
        Box.git_clone(repo_url, init_to_path)
        Box.handle_ignorance(init_to_path)
        click.echo('Unbox successful. Enjoy it!')

    @staticmethod
    def generate_repo_url(box_name: str) -> str:
        if re.match(r'^([a-zA-Z0-9-])+$', box_name):
            repo_url = ['https://github.com/punica-box/', box_name, '-box', '.git']
        elif re.match(r'^([a-zA-Z0-9-])+/([a-zA-Z0-9-])+$', box_name) is None:
            repo_url = ['https://github.com/', box_name, '.git']
        else:
            raise PunicaException(PunicaError.invalid_box_name)
        return ''.join(repo_url)

    @staticmethod
    def unbox(box_name: str, repo_to_path: str = ''):
        repo_url = Box.generate_repo_url(box_name)
        try:
            Box.git_clone(repo_url, repo_to_path)
        except PunicaException as e:
            if e.args[0] == 59000:
                click.echo('Please check out your box name.')
            elif e.args[0]:
                click.echo('This current folder is not NUll.')
                click.echo('Please check out your environment.')
            return
        try:
            Box.handle_ignorance(repo_to_path)
        except PunicaException as e:
            click.echo('Clean work abort...')
            return
        click.echo('Unbox successful. Enjoy it!')

    @staticmethod
    def list_boxes():
        repos_url = 'https://api.github.com/users/punica-box/repos'
        response = requests.get(repos_url).content.decode()
        repos = json.loads(response)
        if isinstance(repos, dict):
            message = repos.get('message', '')
            if 'API rate limit exceeded' in message:
                raise PunicaException(PunicaError.other_error(message))
        name_list = []
        for repo in repos:
            name = repo.get('name', '')
            name_list.append(name)
        return name_list
