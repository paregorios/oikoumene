#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsing Mixins and Utility Classes
"""

import json
import logging
from oikoumene.stringlike import GeographicString
from pathlib import Path
from slugify import slugify
from typing import TextIO, Union

logger = logging.getLogger(__name__)

class StringParser:

    def __init__(
        self,
        delimiter=',',
        output_fieldname='attested'
    ):
        self.delimiter = delimiter
        self.output_fieldname = output_fieldname

    def parse(self, source: Union[TextIO, Path, str, bytes], encoding='utf-8'):
        if isinstance(source, Path):
            values = self._read_file(source, encoding)
        elif isinstance(source, str):
            values = source
        elif isinstance(source, bytes):
            values = source.decode(encoding)
        elif isinstance(source, TextIO):
            values = ''.join(source.readlines())
        else:
            raise TypeError(
                f'Unexpected type ({type(source)}) for "source" argument to parse method. '
                f'Expected {TextIO}, {Path}, {str}, or {bytes}.')
        results = {}
        for v in values.split(self.delimiter):
            if self.output_fieldname != 'romanized':
                gs = GeographicString(romanized=slugify(v, lowercase=False, separator=' '))
                setattr(gs, self.output_fieldname, v)
            else:
                gs = GeographicString(romanized=v)
            try:
                results[gs.id]
            except KeyError:
                results[gs.id] = gs
            else:
                similar = [k for k in results.keys() if k.startswith(gs.id)]
                new_id = f'{gs.id}-{len(similar)}'
                gs.id = new_id
                results[gs.id] = gs
        return results



    def _read_file(self, path: Path, encoding: str):
        with open(path, 'r', encoding=encoding) as fp:
            lines = fp.readlines()
        del fp
        return ''.join(lines)