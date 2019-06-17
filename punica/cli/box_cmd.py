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
    Download a Punica Box, a pre-built Ontology DApp project.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    try:
        Box.unbox(box_name, project_dir)
    except (PunicaException, SDKException) as e:
        echo('An error occur...')
        echo(e.args[1])


@main.command('boxes')
@pass_context
def boxes_cmd(ctx):
    """
    List all available punica box.
    """
    try:
        boxes = Box.list_boxes()
    except (PunicaException, SDKException):
        webbrowser.open('https://punica.ont.io/boxes/')
        return
    echo('The easiest way to get started:')
    for index, box in enumerate(boxes):
        echo(f'{index}. {box}')
