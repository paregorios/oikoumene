#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsing Mixins and Utility Classes
"""

from collections.abc import Sequence
from copy import deepcopy
from io import StringIO, TextIOWrapper
import json
import logging
from oikoumene.place import Place
from oikoumene.stringlike import GeographicName, GeographicString
from pathlib import Path
from pprint import pformat, pprint
from slugify import slugify
from typing import TextIO, Type, Union

logger = logging.getLogger(__name__)

class BaseParser:

    def __init__(self):
        pass

class DictParser(BaseParser):

    def __init__(self, output_type: Union[Type[GeographicString], Type[GeographicName]]=GeographicString):
        BaseParser.__init__(self)
        self.output_type = output_type

    def parse(self, source: Union[dict, Sequence[dict]]) -> Union[Type[GeographicString], Type[GeographicName]]:
        if isinstance(source, dict):
            values = [source]
        elif isinstance(source, Sequence):
            values = list(source)
        else:
            raise TypeError(
                f'Unexpected type ({type(source)}) for "source" argument to parse method. '
                f'Expected {dict} or a sequence of {dict}.')
        results = {}
        for v in values:
            try:
                v['romanized']
            except KeyError:
                try:
                    a = v['attested']
                except KeyError:
                    pass  # let the GeographicString constructor handle the omission
                else:
                    v['romanized'] = slugify(a, lowercase=False, separator=' ')
            gs = self.output_type(**v)
            gs.make_unique_id(list(results.keys()))
            results[gs.id] = gs
        return results

class StringParser(BaseParser):

    def __init__(
        self,
        delimiter: str=',',
        output_type: Union[Type[GeographicString], Type[GeographicName]]=GeographicString,
        output_fieldname: str='attested'
    ):
        BaseParser.__init__(self)
        self.delimiter = delimiter
        self.output_type = output_type
        self.output_fieldname = output_fieldname

    def parse(self, source: Union[TextIOWrapper, StringIO, Path, str, bytes], encoding='utf-8') -> Union[Type[GeographicString], Type[GeographicName]]:
        if isinstance(source, Path):
            values = self._read_file(source, encoding)
        elif isinstance(source, str):
            values = source
        elif isinstance(source, bytes):
            values = source.decode(encoding)
        elif isinstance(source, (TextIOWrapper, StringIO)):
            values = ''.join(source.readlines()).strip()
        else:
            raise TypeError(
                f'Unexpected type ({type(source)}) for "source" argument to parse method. '
                f'Expected {TextIO}, {Path}, {str}, or {bytes}.')
        results = {}
        for v in values.split(self.delimiter):
            logger.debug(f'v: {v}')
            if self.output_fieldname != 'romanized':
                gs = self.output_type(romanized=slugify(v, lowercase=False, separator=' '))
                setattr(gs, self.output_fieldname, v)
            else:
                gs = self.output_type(romanized=v)
            gs.make_unique_id(list(results.keys()))
            results[gs.id] = gs
        return results

    def _read_file(self, path: Path, encoding: str):
        with open(path, 'r', encoding=encoding) as fp:
            lines = fp.readlines()
        del fp
        return ''.join(lines).strip()
