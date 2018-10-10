#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .main import main

from punica.invoke.invoke_contract import Invoke


@main.command('invoke')
@click.option('--network', nargs=1, type=str, default='', help='Specify which network the contract will be deployed.')
@click.option('--wallet', nargs=1, type=str, default='', help='Specify which wallet file will be used.')
@click.pass_context
def invoke_cmd(ctx, network, wallet):
    """
    Invoke the function list in punica-config.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Invoke.invoke_all_function_in_list(wallet, project_dir, network)
