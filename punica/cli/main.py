#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pkg_resources

import click

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--project',
    '-p',
    'project_dir',
    help=(
            "Specify a punica project directory."
    ),
    type=click.Path(exists=False, dir_okay=True),
)
# @click.version_option(
#     pkg_resources.get_distribution("punica").version,
#     '--version',
#     '-v',
#     message='%(version)s',
# )
@click.pass_context
def main(ctx, project_dir):
    ctx.obj = dict()
    if project_dir is None:
        project_dir = os.getcwd()
    ctx.obj['PROJECT_DIR'] = project_dir


if __name__ == '__main__':
    main()
