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
            try:
                result = self._parse(parts)
            except NotImplementedError:
                print('This feature is not yet implemented.')
            else:
                print(result)

    def _parse(self, parts: list=[], verb: str='', object: str='', options: list=[]):
        if verb and not object and len(parts) == 0:
            try:
                return getattr(self, f'_v_{verb.lower()}')()
            except TypeError:
                return 'Syntax error:\n' + self._usage(verb)
            except AttributeError:
                return f'Unknown command "{verb}". Type "help" for list of commands.'
        elif not verb and not object:
            m = rx_integer.match(parts[0])
            if m:
                return self._parse(parts[1:], object=parts[0])
            else:
                return self._parse(parts[1:], verb=parts[0])
        elif verb and not object:
            return self._parse(verb=verb, object=parts[-1], options=parts[:-1])
        elif verb and object:
            try:
                return getattr(self, f'_v_{verb.lower()}')(object=object, options=options)
            except TypeError as err:
                return 'Syntax error:\n' + self._usage(verb)
            except AttributeError:
                return f'Unknown command "{verb}"". Type "help" for list of commands.'
        elif not verb and object:
            if len(parts) == 0 and len(options) == 0:
                return self._parse(verb='examine', object=object)
            else:
                raise RuntimeError('barf')
        else:
            raise RuntimeError('panic')

    def _usage(self, verb: str):
        v = verb.lower()
        doc = getdoc(getattr(self, f'_v_{v}'))
        try:
            usage = getattr(self, f'_usage_{v}')()
        except AttributeError:
            usage = []
        if usage:
            usage.insert(0, '\n  Usage:')
            usage = '\n  '.join(usage)
        else:
            usage = ''
        msg = f'{v}: {doc}' + usage
        return msg.strip()

    def _usage_examine(self):
        return ['examine {context number}']

    def _usage_find(self):
        return [
            'find {search string}+'
        ]

    def _usage_load(self):
        return [
            'load {filepath}',
            'load {filepath} {format=json|txt}'
        ]

    def _usage_save(self):
        return [
            'save {filepath}',
            'save {filepath} {format=json|txt}'
        ]

    def _v_contents(self):
        """List contents of the gazetteer."""
        return self.manager.contents()

    def _v_drop(self):
        """Erase contents of the gazetteer from memory."""
        return self.manager.drop()
    
    def _v_examine(self, object: str, options: list):
        """Examine a single gazetteer object from the most recent "contents" listing."""
        if options:
            raise TypeError(options)
        return self.manager.examine(object)

    def _v_find(self, object: str, options: list):
        """Search the gazetteer for matching character strings."""
        if options:
            raise NotImplementedError(options)
        return self.manager.find(object)

    def _v_help(self, object: str='', options: list=[]):
        """List available commands."""
        if object:
            return self._usage(object)
        else:
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
        try:
            return self.manager.load(object, format)
        except FileNotFoundError as err:
            return str(err)

    def _v_list(self):
        """List contents of the gazetteer."""
        return self._v_contents()

    def _v_ls(self):
        """List contents of the gazetteer."""
        return self._v_contents()

    def _v_save(self, object: str, options: list):
        """Save gazetteer content to a file."""
        format = ''
        if options:
            if len(options) == 1:
                format=options[0]
            else:
                raise NotImplementedError(options)
        else:
            format = object.split('.')[-1]
        return self.manager.save(object, format)

    def _v_q(self):
        """Quit interactive interface."""
        self._v_quit()

    def _v_quit(self):
        """Quit interactive interface."""
        exit()

        
