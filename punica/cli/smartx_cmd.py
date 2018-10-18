#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .main import main


@main.command('smartx')
@click.pass_context
def smartx_cmd(ctx):
    """
    Ontology smart contract IDE,SmartX (http://smartx.ont.io/)
    """
    print()
    print('Please go to Smartx for debugging smart contracts: \nhttp://smartx.ont.io/#/')
    print()
