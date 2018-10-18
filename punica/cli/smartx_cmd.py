#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .main import main


@main.command('smartx')
@click.pass_context
def smartx_cmd(ctx):
    """
    Please go to smartx for debugging smart contracts: http://smartxdebug.ont.io/#/
    """
    pass
