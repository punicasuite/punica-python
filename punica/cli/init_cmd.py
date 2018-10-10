#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .main import main

from punica.box.repo_box import Box


@main.command('init')
@click.pass_context
def init_cmd(ctx):
    """
    Initialize new and empty Ontology DApp project.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    Box.init(project_dir)
