#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2015. The Koodous Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import io
import json
import logging
import os

import click

from koodous import Koodous
from utils import pygmentize_json

__author__ = "Federico Maggi <federico.maggi@gmail.com>"

logger = logging.getLogger('koocli')

LOGGING_LEVELS = dict((
    ('notset', logging.NOTSET),
    ('debug', logging.DEBUG),
    ('info', logging.INFO),
    ('warning', logging.WARNING),
    ('error', logging.ERROR),
    ('critical', logging.CRITICAL),
))

loglevels = LOGGING_LEVELS.keys()


@click.group()
@click.option('--quiet/--no-quiet', default=False,
              help='Suppress output (logging is configured separately)')
@click.option('--wdir', type=click.Path(exists=False), required=True,
              help='Working directory')
@click.option('--loglevel', type=click.Choice(loglevels), default='info')
@click.option('--token', envvar='TOKEN', help='Koodous API token',
              required=True)
def cli(quiet, loglevel, wdir, token):
    """A simple command line interface (CLI) to the Koodous API.

    In order to use this CLI, you need an account at koodous.com and you
    need to grab your API token at https://koodous.com/settings/profile

    You can pass the API token both as a command line option, or set it as
    an environment variable (TOKEN).

    \b To get help for each individual command, just type

        $ koocli <command_name> --help

    """
    ctx = click.get_current_context()

    ctx.meta['TOKEN'] = token
    ctx.meta['api'] = Koodous(token=token)
    ctx.meta['wdir'] = wdir
    ctx.meta['quiet'] = quiet

    import coloredlogs
    coloredlogs.install(level=LOGGING_LEVELS[loglevel])


@cli.command()
@click.option('--save/--no-save', default=False,
              help='Save JSON to file in the working directory')
@click.option('--outfile', help='Optional file to save the metadata to',
              type=click.File('wb'))
@click.argument('ruleset_id', type=int)
def get_public_ruleset(save, outfile, ruleset_id):
    """Get a public ruleset by its RULESET_ID"""
    ctx = click.get_current_context()

    api = ctx.meta.get('api')
    wdir = ctx.meta.get('wdir')
    quiet = ctx.meta.get('quiet')

    logger.info('Attempting to fetch ruleset %s', ruleset_id)
    result = api.get_public_ruleset(ruleset_id=ruleset_id)

    if not quiet:
        click.echo(pygmentize_json(result))

    if save:
        if not outfile:
            filepath = os.path.join(wdir, 'ruleset-{}.json'.format(ruleset_id))
            outfile = io.open(filepath, 'wb')
        else:
            filepath = outfile.name
        logger.info('Saving ruleset metadata to {}'.format(filepath))

        json.dump(result, outfile)

        logger.info('Ruleset metadata saved correctly')


@cli.command()
@click.option('--save/--no-save', default=False,
              help='Save output as separate JSON files in the working '
                   'directory')
@click.option('--download/--no-download', default=False,
              help='Download the actual APK files and save them in the '
                   'working directory')
@click.option('--prompt/--no-prompt', default=True,
              help='Prompt for confirmations')
@click.option('--limit', type=int, default=0, help='Stop after LIMIT matches')
@click.argument('ruleset_id', type=int)
def get_matches_public_ruleset(prompt, save, download, limit, ruleset_id):
    """Get the APKs that match a public ruleset by its RULESET_ID"""
    ctx = click.get_current_context()

    api = ctx.meta.get('api')
    quiet = ctx.meta.get('quiet')
    wdir = ctx.meta.get('wdir')

    logger.info('Attempting to fetch ruleset %s', ruleset_id)
    ruleset = api.get_public_ruleset(ruleset_id=ruleset_id)

    d = ruleset['detections']

    if save:
        filepath = os.path.join(wdir, 'ruleset-{}.json'.format(
            ruleset_id))

        logger.info('Saving ruleset to %s', filepath)
        with io.open(filepath, 'wb') as outfile:
            json.dump(ruleset, outfile)

        logger.info('Ruleset saved successfully')

    if prompt and 100 < d <= limit:
        if not click.confirm('The selected ruleset has {} matches. Do you '
                             'want to proceed printing all of '
                             'them?'.format(d)):
            return

    iterator = api.iter_matches_public_ruleset(ruleset_id)
    count = 0

    for apks in iterator:
        for apk in apks:
            if not quiet:
                click.echo(pygmentize_json(apk))

            if save:
                sha256 = apk['sha256']

                filepath = os.path.join(wdir, '{}.json'.format(sha256))

                logger.info('Saving metadata of %s to %s', sha256, filepath)

                with io.open(filepath, 'wb') as outfile:
                    json.dump(apk, outfile)

            if download:
                dst = os.path.join(wdir, '{}.apk'.format(sha256))
                logger.info('Downloading %s to %s', sha256, dst)

                api.download_to_file(sha256=sha256, dst=dst)

                logger.info('APK downloaded successfully')

            count += 1

            if count >= limit:
                logger.info('Limit of %s matches reached: stopping!', limit)
                break
        if count >= limit:
            break
