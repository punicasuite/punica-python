
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .main import main


@main.command('scpm')
@click.pass_context
def scpm_cmd(ctx):
    """
    smart contract package manager，support download and publish.
    """
    print('Usage: punica scpm [OPTIONS]')
    print('')
    print('  ', 'smart contract package manager，support download and publish.')
    print()
    print('Options:')
    print('  ', '-h, --help  Show this message and exit.')
    print()
