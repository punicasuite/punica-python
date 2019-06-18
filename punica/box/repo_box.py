#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

from os import listdir, getcwd, path

from click import echo
import requests

from halo import Halo
from git import RemoteProgress, Repo, GitCommandError

from punica.utils.file_system import (
    ensure_remove_dir_if_exists,
    remove_file_if_exists,
    ensure_path_exists
)

from punica.exception.punica_exception import PunicaError, PunicaException


class Box:
    @staticmethod
    def handle_ignorance(repo_to_path: str = '') -> bool:
        unpack_spinner = Halo(text="Unpacking...", spinner='dots')
        unpack_spinner.start()
        box_ignore_file_path = path.join(repo_to_path, 'punica-box.json')
        try:
            with open(box_ignore_file_path, 'r') as f:
                box_ignore_files = json.load(f)['ignore']
            remove_file_if_exists(box_ignore_file_path)
        except FileNotFoundError:
            unpack_spinner.fail()
            return False
        for file in box_ignore_files:
            try:
                file_path = path.join(repo_to_path, file)
                ensure_remove_dir_if_exists(file_path)
                remove_file_if_exists(file_path)
            except (PermissionError, FileNotFoundError):
                unpack_spinner.fail()
                return False
        unpack_spinner.succeed()
        return True

    @staticmethod
    def prepare_to_download(box_name: str, to_path: str = '') -> str:
        prepare_spinner = Halo(text="Preparing to download", spinner='dots')
        prepare_spinner.start()
        if to_path == '':
            to_path = getcwd()
        ensure_path_exists(to_path)
        if listdir(to_path):
            prepare_spinner.fail()
            echo('This directory is non-empty...')
            return ''
        repo_url = Box.generate_repo_url(box_name)
        if requests.get(repo_url).status_code != 200:
            echo('Please check the box name you input.')
            prepare_spinner.fail()
            return ''
        prepare_spinner.succeed()
        return repo_url

    @staticmethod
    def echo_unbox_failed():
        echo('Unbox failed.')

    @staticmethod
    def echo_unbox_successful():
        echo('\nUnbox successful. Sweet!')

    @staticmethod
    def init(to_path: str):
        repo_url = Box.prepare_to_download('punica-init-default', to_path)
        if len(repo_url) == 0:
            Box.echo_unbox_failed()
            return False
        if not Box.download_repo(repo_url, to_path):
            Box.echo_unbox_failed()
            return False
        Box.handle_ignorance(to_path)
        Box.echo_unbox_successful()
        Box.echo_box_help_cmd()
        return True

    @staticmethod
    def unbox(box_name: str, to_path: str = '') -> bool:
        repo_url = Box.prepare_to_download(box_name, to_path)
        if len(repo_url) == 0:
            Box.echo_unbox_failed()
            return False
        if Box.download_repo(repo_url, to_path):
            Box.handle_ignorance(to_path)
            Box.echo_unbox_successful()
            Box.echo_box_help_cmd()
            return True
        Box.echo_unbox_failed()
        return False

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
    def download_repo(repo_url: str, repo_to_path: str = ''):
        if repo_to_path == '':
            repo_to_path = getcwd()
        spinner = Halo(spinner='dots')

        def calcu_progress_scale(cur_count: int, max_count: int):
            return round(cur_count / max_count * 100, 2)

        def show_spinner(stage_info: str, cur_count: int, max_count: int, message: str = ''):
            if spinner.spinner_id is None:
                spinner.start()
            scale = calcu_progress_scale(cur_count, max_count)
            if len(message) == 0:
                spinner.text = f'{stage_info}: {scale}% ({cur_count}/{max_count})'
            else:
                spinner.text = f'{stage_info}: {scale}%, {message}'
            if scale == 100:
                spinner.succeed()
            return

        def update(self, op_code: RemoteProgress, cur_count: int, max_count: int = None, message: str = ''):
            if op_code == RemoteProgress.COUNTING:
                show_spinner('Counting objects', cur_count, max_count)
                return
            if op_code == RemoteProgress.COMPRESSING:
                show_spinner('Compressing objects', cur_count, max_count)
                return
            if op_code == RemoteProgress.RECEIVING:
                show_spinner('Receiving objects', cur_count, max_count, message)
                return
            if op_code == RemoteProgress.RESOLVING:
                show_spinner('Resolving deltas', cur_count, max_count)
                return
            if op_code == RemoteProgress.WRITING:
                show_spinner('Writing objects', cur_count, max_count)
                return
            if op_code == RemoteProgress.FINDING_SOURCES:
                show_spinner('Finding sources', cur_count, max_count)
                return
            if op_code == RemoteProgress.CHECKING_OUT:
                show_spinner('Checking out files', cur_count, max_count)
                return

        RemoteProgress.update = update

        try:
            Repo.clone_from(url=repo_url, to_path=repo_to_path, depth=1, progress=RemoteProgress())
            if spinner.spinner_id is not None and len(spinner.text) != 0:
                spinner.fail()
                return False
            return True
        except GitCommandError as e:
            if spinner.spinner_id is not None and len(spinner.text) != 0:
                spinner.fail()
            if e.status == 126:
                echo('Please check your network.')
            elif e.status == 128:
                echo('Please check your Git tool.')
            else:
                raise PunicaException(PunicaError.other_error(e.args[2]))
            return False

    @staticmethod
    def echo_box_help_cmd():
        echo('\nCommands:\n'
             '  Compile contracts: punica compile\n'
             '  Deploy contracts : punica deploy\n'
             '  Test contracts   : punica test\n')

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
