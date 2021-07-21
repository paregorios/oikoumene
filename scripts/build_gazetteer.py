#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a gazetteer from basic data.    
"""

from airtight.cli import configure_commandline
import json
import logging
from oikoumene.gazetteer import Gazetteer
from oikoumene.parsing import StringParser
from pathlib import Path
from pprint import pformat
import sys

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    ['-l', '--loglevel', 'NOTSET',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR',
        False],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)',
        False],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)', False],
    ['-i', '--input_file', '', 'path to input file', False],
    ['-if', '--input_format', 'txt', 'input file format', False],
    ['-o', '--output_file', '', 'path to output file', False],
    ['-of', '--output_format', 'json', 'output file format', False]
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]

def make_gaz(input_file='', input_format='', **kwargs):
    path = Path(input_file).expanduser().resolve()
    with open(path, 'r', encoding='utf-8') as f:
        if input_format == 'json':            
            data = json.load(f)
        elif input_format == 'txt':
            parser = StringParser(delimiter='\n')
            data = parser.parse(f)
        else:
            raise NotImplementedError(input_format)
    del f
    return Gazetteer(data)

def output_gaz(gaz, output_file='', output_format='', **kwargs):
    if output_format == 'json':
        result = gaz.json()
    elif output_format == 'txt':
        result = str(gaz)
    else:
        raise NotImplementedError(output_format)
    if output_file == '':
        print(result)
    else:
        path = Path(output_file).expanduser().resolve()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(result)
        del f

def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    if not(kwargs['input_file']):
        raise NotImplementedError('Interactive mode not supported. Specify --input_file.')
    g = make_gaz(**kwargs)
    output_gaz(g, **kwargs)

if __name__ == "__main__":
    main(**configure_commandline(
        OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
