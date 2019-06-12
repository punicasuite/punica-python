#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import webbrowser

from .main import main


@main.command('solo')
@click.pass_context
def solo_chain_cmd(ctx):
    """
    Ontology Blockchain private net in test mode. please download from https://github.com/punicasuite/solo-chain/releases
    """
    webbrowser.open('https://github.com/punicasuite/solo-chain/releases')
