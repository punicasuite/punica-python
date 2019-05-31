#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json

import git
import click
import requests

from punica.utils.file_system import (
    ensure_remove_dir_if_exists,
    remove_file_if_exists,
    ensure_path_exists
)

from punica.exception.punica_exception import PunicaError, PunicaException


class Box:
    @staticmethod
    def handle_ignorance(repo_to_path: str = ''):
        click.echo('Unpacking...')
        box_ignore_file_path = os.path.join(repo_to_path, 'punica-box.json')
        try:
            with open(box_ignore_file_path, 'r') as f:
                box_ignore_files = json.load(f)['ignore']
        except FileNotFoundError:
            return
        remove_file_if_exists(box_ignore_file_path)
        for file in box_ignore_files:
            try:
                file_path = os.path.join(repo_to_path, file)
                ensure_remove_dir_if_exists(file_path)
                remove_file_if_exists(file_path)
            except (PermissionError, FileNotFoundError):
                pass

    @staticmethod
    def git_clone(repo_url: str, repo_to_path: str = ''):
        if repo_to_path == '':
            repo_to_path = os.getcwd()
        if os.listdir(repo_to_path):
            raise PunicaException(PunicaError.file_exist_error)
        click.echo('Downloading...')
        try:
            git.Repo.clone_from(url=repo_url, to_path=repo_to_path, depth=1)
        except git.GitCommandError as e:
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
