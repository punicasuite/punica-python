#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .main import main

from punica.box.repo_box import Box
from ontology.exception.exception import SDKException
from punica.exception.punica_exception import PunicaException


@main.command('unbox')
@click.argument('box_name', nargs=1)
@click.pass_context
def unbox_cmd(ctx, box_name):
    """
    Download a Punica Box, a pre-built Ontology DApp project.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        Box.unbox(box_name, project_dir)
    except (PunicaException, SDKException):
        print('An error occur...')
        exit(1)
