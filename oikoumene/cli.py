#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Line Interface
"""

from inspect import getdoc
import logging
from oikoumene.normalization import norm
from oikoumene.manager import Manager
import re

logger = logging.getLogger(__name__)
rx_integer = re.compile(r'^\d+$')
class CLI:

    def __init__(self):
        self.manager = Manager()

    def interact(self):
        while True:
            s = norm(input('> '))
            parts = s.split()
            result = self._parse(parts)
            print(result)

    def _parse(self, parts: list=[], verb: str='', object: str='', options: list=[]):
        if verb and not object and len(parts) == 0:
            return getattr(self, f'_v_{verb.lower()}')()
        elif not verb and not object:
            m = rx_integer.match(parts[0])
            if m:
                raise NotImplementedError()
            else:
                return self._parse(parts[1:], verb=parts[0])
        elif verb and not object:
            m = rx_integer.match(parts[-1])
            if m:
                raise NotImplementedError()
            else:
                return self._parse(verb=verb, object=parts[-1], options=parts[:-1])
        elif verb and object:
            return getattr(self, f'_v_{verb.lower()}')(object=object, options=options)

    def _v_contents(self):
        """List contents of the gazetteer."""
        return self.manager.contents()

    def _v_drop(self):
        """Erase contents of the gazetteer from memory."""
        return self.manager.drop()

    def _v_find(self, object: str, options: list):
        """Search the gazetteer for matching character strings."""
        if options:
            raise NotImplementedError(options)
        return self.manager.find(object)

    def _v_help(self):
        """List available commands."""
        methods = [k for k in dir(self) if k.startswith('_v_')]
        entries = [(k.split('_')[-1], getdoc(getattr(self, k))) for k in methods]
        entries.sort(key=lambda x: x[0])
        longest = max([len(e[0]) for e in entries])
        entries = [f'{e[0]}:'.rjust(longest+1) + f' {e[1]}' for e in entries]
        return '\n'.join(entries)

    def _v_json(self):
        """List gazetteer contents in JSON format (see "save" to write to file)."""
        return self.manager.json()

    def _v_len(self):
        """Count number of objects in the gazetteer."""
        return self.manager.len()

    def _v_load(self, object: str, options: list):
        """Load gazetteer content from file."""
        format = ''
        if options:
            if len(options) == 1:
                format=options[0]
            else:
                raise NotImplementedError(options)            
        else:
            format = object.split('.')[-1]
        return self.manager.load(object, format)

    def _v_list(self):
        """List contents of the gazetteer."""
        return self._contents()

    def _v_ls(self):
        """List contents of the gazetteer."""
        return self._contents()


        
