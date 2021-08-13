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
        entries = [(id, obj.label) for id, obj in objs.items()]
        rx = re.compile(r'[,\(\)\s]+')
        entries.sort(key=lambda x: rx.sub('', x[1]).lower())
        self._context = OrderedDict()
        for i, entry in enumerate(entries):
            self._context[str(i+1)] = entry
        return '\n'.join([f'{k}: {v[1]}' for k, v in self._context.items()])

    def contents(self):
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        return self._ordered_list(self.gaz.contents)

    def drop(self):
        """Erase the contents of the current gazetteer from memory."""
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        g = self.gaz
        self.gaz = None
        self._context = None
        count = len(g.contents)
        del g
        return f'Erased current gazetteer from memory ({count} objects).'

    def examine(self, context_number):
        """Examine a single object in the gazetteer."""
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        id, label = self._context[context_number]
        obj = self.gaz.contents[id]
        return f'{label}\n{obj.json()}'

    def find(self, search_string: str):
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        entries = self.gaz.get({'text': search_string}, operator='or')
        return self._ordered_list(entries)

    def json(self):
        """Get JSON representation of gazetteer."""
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        return self.gaz.json()

    def len(self):
        """Get number of objects in the gazetteer."""
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        return f'There are {len(self.gaz.contents)} objects in the gazetteer.'

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

    def merge(self, context_numbers: list):
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        print(f'context numbers: {context_numbers}')
        ids = [self._context[n][0] for n in context_numbers]
        print(f'ids: {ids}')
        id = self.gaz.merge(ids)
        obj = self.gaz.contents[id]
        self._context = None
        return f'Merged {len(ids)} objects to new object "{str(obj)}":\n{obj.json()}'

    def remove(self, context_number):
        """Remove a single object from the gazetteer."""
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        id, label = self._context[context_number]
        self.gaz.remove(id)
        self._context = None
        return f'Removed "{label}" object from the gazetteer.'

    def save(self, output_path: str, output_format: str='json'):
        """Save a gazetteer to file."""
        if self.gaz is None:
            return 'No gazetteer is loaded.'
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
        if self.gaz is None:
            return 'No gazetteer is loaded.'
        return str(self.gaz)


