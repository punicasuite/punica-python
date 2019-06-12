#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import webbrowser
from os import listdir

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
    except (PunicaException, SDKException) as e:
        click.echo('An error occur...')
        click.echo(e.args[1])


@main.command('boxes')
@click.pass_context
def boxes_cmd(ctx):
    """
    List all available punica box.
    """
    try:
        boxes = Box.list_boxes()
    except (PunicaException, SDKException) as e:
        webbrowser.open('https://punica.ont.io/boxes/')
        return
    click.echo('Various punica boxes are waiting for your:')
    for box in boxes:
        click.echo('\t', box)
