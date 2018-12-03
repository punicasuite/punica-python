#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import webbrowser

from .main import main


@main.command('smartx')
@click.pass_context
def smartx_cmd(ctx):
    """
    Ontology smart contract IDE,SmartX (http://smartx.ont.io/)
    """
    webbrowser.open("https://smartx.ont.io/")
