#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from ontology.exception.exception import SDKException

from .main import main

from punica.box.repo_box import Box
from punica.exception.punica_exception import PunicaException


@main.command('init')
@click.pass_context
def init_cmd(ctx):
    """
    Initialize new and empty Ontology DApp project.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        Box.init(project_dir)
    except (PunicaException, SDKException) as e:
        print('An error occur...')
        print(e)
        print('Punica will exist...')
        exit(1)
