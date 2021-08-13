#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manager
"""

from collections import OrderedDict
import json
import logging
from oikoumene.gazetteer import Gazetteer
from oikoumene.parsing import StringParser

from pathlib import Path
import re

logger = logging.getLogger(__name__)

class Manager:

    def __init__(self):
        self.gaz = None
        self._context = None

    def _ordered_list(self, objs: dict):
        entries = [(id, obj.strings()) for id, obj in objs.items()]
        rx = re.compile(r'[,\(\)\s]+')
        entries.sort(key=lambda x: rx.sub('', x[1]).lower())
        self._context = OrderedDict()
        for i, entry in enumerate(entries):
            self._context[str(i+1)] = entry[1]
        return '\n'.join([f'{k}: {v}' for k, v in self._context.items()])

    def contents(self):
        return self._ordered_list(self.gaz.contents)

    def drop(self):
        """Erase the contents of the current gazetteer from memory."""
        g = self.gaz
        self.gaz = None
        self._context = None
        count = len(g.contents)
        del g
        return f'Erased current gazetteer from memory ({count} objects).'

    def find(self, search_string: str):
        entries = self.gaz.get({'text': search_string}, operator='or')
        return self._ordered_list(entries)

    def json(self):
        """Get JSON representation of gazetteer."""
        return self.gaz.json()

    def len(self):
        """Get number of objects in the gazetteer."""
        return len(self.gaz.contents)

    def load(self, input_path: str, input_format: str='json'):
        """Load a gazetteer from file."""
        if isinstance(input_path, Path):
            path = input_path.expanduser().resolve()
        elif isinstance(input_path, str):
            path = Path(input_path).expanduser().resolve()
        else:
            raise TypeError(type(input_path))
        with open(path, 'r', encoding='utf-8') as f:
            if input_format == 'json':            
                data = json.load(f)
            elif input_format == 'txt':
                parser = StringParser(delimiter='\n')
                data = parser.parse(f)
            else:
                raise NotImplementedError(input_format)
        del f
        self.gaz = Gazetteer(data)
        return f'Read {len(self.gaz.contents)} objects from {path}.'

    def save(self, output_path: str, output_format: str='json'):
        """Save a gazetteer to file."""
        if output_format == 'json':
            result = self.gaz.json()
        elif output_format == 'txt':
            result = str(self.gaz)
        else:
            raise NotImplementedError(output_format)
        path = Path(output_path).expanduser().resolve()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(result)
        del f
        return f'Saved {len(self.gaz.contents)} objects to {path}.'

    def str(self):
        """Get string representation of gazetteer."""
        return str(self.gaz)


