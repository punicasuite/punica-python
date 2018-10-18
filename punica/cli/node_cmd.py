#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .main import main


@main.command('node')
@click.pass_context
def node_cmd(ctx):
    """
    Ontology Blockchain private net in test mode. please download from https://github.com/punicasuite/solo-chain/releases
    """
    pass
