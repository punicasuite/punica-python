#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from punica.tool.tool import Tool

from .main import main

from punica.exception.punica_exception import PunicaException


@main.group('tool', invoke_without_command=True)
@click.pass_context
def tool_cmd(ctx):
    """
    Unit test with specified smart contract
    """
    if ctx.invoked_subcommand is None:
        project_dir = ctx.obj['PROJECT_DIR']
    else:
        pass


@tool_cmd.command('transform')
@click.option('--addresstohex', nargs=1, type=str, default='', help='transform address to hex.')
@click.option('--stringtohex', nargs=1, type=str, default='', help='transform string to hex.')
@click.option('--hexreverse', nargs=1, type=str, default='', help='hex string reverse.')
@click.option('--numtohex', nargs=1, type=str, default='', help='transform num to hex.')
@click.option('--generateprivatekey', nargs=1, type=str, default='', help='generate private key.')
@click.pass_context
def transform_cmd(addresstohex, stringtohex, hexreverse, numtohex, generateprivatekey):
    """
    transform data
    """
    if addresstohex != '':
        Tool.address_to_hex(addresstohex)
    if stringtohex != '':
        Tool.str_to_hex(stringtohex)
    if hexreverse != '':
        Tool.hex_reverse(hexreverse)
    if numtohex != '':
        Tool.num_to_hex(numtohex)
    if generateprivatekey != '':
        Tool.generate_random_private_key()


@tool_cmd.command('decryptprivatekey')
@click.option('--key', nargs=1, type=str, default='', help='encrypted private key.')
@click.option('--address', nargs=1, type=str, default='', help='address.')
@click.option('--salt', nargs=1, type=str, default='', help='salt.')
@click.option('--n', nargs=1, type=str, default='', help='n.')
@click.option('--password', nargs=1, type=str, default='', help='password.')
def decryptprivatekey():
    Tool.decrypt_private_key()





