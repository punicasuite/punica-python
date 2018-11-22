#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from punica.tool.tool import Tool

from .main import main


@main.group('tool', invoke_without_command=True)
@click.pass_context
def tool_cmd(ctx):
    """
    Data format conversion tool
    """
    if ctx.invoked_subcommand is None:
        print('Usage: punica tool [OPTIONS] COMMAND [ARGS]...')
        print('')
        print('  ', 'Data format conversion tool.')
        print()
        print('Options:')
        print('  ', '-h, --help  Show this message and exit.')
        print()
        print('Commands:')
        print('  ', 'decryptprivatekey  decrypt privatekey')
        print('  ', 'transform          transform data')
    else:
        pass


@tool_cmd.command('transform')
@click.option('--addresstohex', nargs=1, type=str, default='', help='transform address to hex.')
@click.option('--stringtohex', nargs=1, type=str, default='', help='transform string to hex.')
@click.option('--hexreverse', nargs=1, type=str, default='', help='hex string reverse.')
@click.option('--numtohex', nargs=1, type=int, default=0, help='transform num to hex.')
def transform_cmd(addresstohex, stringtohex, hexreverse, numtohex):
    """
    transform data
    """
    if addresstohex != '':
        Tool.address_to_hex(addresstohex)
    elif stringtohex != '':
        Tool.str_to_hex(stringtohex)
    elif hexreverse != '':
        Tool.hex_reverse(hexreverse)
    elif numtohex != '':
        Tool.num_to_hex(numtohex)
    else:
        print('Usage: punica tool transform [OPTIONS]')
        print('')
        print('  ', 'transform data.')
        print()
        print('Options:')
        print('  ', '--addresstohex TEXT  transform address to hex.')
        print('  ', '--stringtohex TEXT   transform string to hex.')
        print('  ', '--hexreverse TEXT    hex string reverse.')
        print('  ', '--numtohex TEXT      transform num to hex.')
        print('  ', '-h, --help           Show this message and exit.')
        print()


@tool_cmd.command('generateprivatekey')
def decryptprivatekey_cmd(key, address, salt, n, password):
    """
    generate random privatekey
    """
    Tool.generate_random_private_key()


@tool_cmd.command('decryptprivatekey')
@click.option('--key', nargs=1, type=str, default='', help='encrypted private key.')
@click.option('--address', nargs=1, type=str, default='', help='address.')
@click.option('--salt', nargs=1, type=str, default='', help='salt.')
@click.option('--n', nargs=1, type=int, default=16384, help='n.')
@click.option('--password', nargs=1, type=str, default='', help='password.')
def decryptprivatekey_cmd(key, address, salt, n, password):
    """
    decrypt privatekey
    """
    if key == '' and address == '' and salt == '' or n == 0 and password == '':
        print('Usage: punica tool decryptprivatekey [OPTIONS]')
        print('')
        print('  ', 'decrypt privatekey')
        print()
        print('Options:')
        print('  ', '--key TEXT       encrypted private key.')
        print('  ', '--address TEXT   address.')
        print('  ', '--salt TEXT      salt.')
        print('  ', '--n TEXT         n.')
        print('  ', '--password TEXT  password.')
        print('  ', '-h, --help       Show this message and exit.')
        print()
        return
    if key == '':
        print('Error:')
        print('key should not be \'\'')
        return
    if address == '':
        print('Error:')
        print('address should not be \'\'')
        return
    if salt == '':
        print('Error:')
        print('salt should not be \'\'')
        return
    if password == '':
        print('Error:')
        print('password should not be \'\'')
        return
    Tool.decrypt_private_key(key, address, salt, n, password)





