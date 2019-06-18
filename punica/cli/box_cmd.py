#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser

from click import echo, argument, pass_context
from ontology.exception.exception import SDKException

from .main import main
from punica.box.repo_box import Box
from punica.exception.punica_exception import PunicaException


@main.command('unbox')
@argument('box_name', nargs=1)
@pass_context
def unbox_cmd(ctx, box_name):
    """
    Download a Punica Box, a pre-built Punica project
    """
    box = Box(ctx.obj['PROJECT_DIR'])
    try:
        box.unbox(box_name)
    except (PunicaException, SDKException) as e:
        echo('An error occur...')
        echo(e.args[1])


@main.command('init')
@pass_context
def init_cmd(ctx):
    """
    Initialize new and empty Ontology project.
    """
    box = Box(ctx.obj['PROJECT_DIR'])
    try:
        box.init_box()
    except (PunicaException, SDKException) as e:
        echo('An error occur...')
        echo(e.args[1])


@main.command('boxes')
@pass_context
def boxes_cmd(ctx):
    """
    List all available punica box.
    """
    box = Box(ctx.obj['PROJECT_DIR'])
    try:
        box.list_boxes()
    except (PunicaException, SDKException):
        webbrowser.open('https://punica.ont.io/boxes/')
        return
