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
import shlex

logger = logging.getLogger(__name__)
rx_integer = re.compile(r'^\d+$')
rx_integer_range = re.compile(r'^(?P<start>\d+)\s*\-\s*(?P<end>\d+)$')
class CLI:

    def __init__(self):
        self.manager = Manager()

    def interact(self):
        while True:
            s = norm(input('> '))
            parts = shlex.split(s)
            try:
                result = self._parse(parts)
            except NotImplementedError as err:
                print(f'This feature is not yet implemented: {str(err)}.')
            else:
                print(result)

    def _parse(self, parts: list=[], verb: str='', object: str='', options: list=[]):
        if verb and not object and len(parts) == 0:
            try:
                return getattr(self, f'_v_{verb.lower()}')()
            except TypeError as err:
                logger.error(str(err))
                return 'Syntax error:\n' + self._usage(verb)
            except AttributeError as err:
                logger.error(str(err))
                return f'Unknown command "{verb}". Type "help" for list of commands.'
        elif not verb and not object:
            m = rx_integer.match(parts[0])
            if m:
                return self._parse(parts[1:], object=parts[0])
            else:
                return self._parse(parts[1:], verb=parts[0])
        elif verb and not object:
            return self._parse(verb=verb, object=parts[0], options=parts[1:])
        elif verb and object:
            try:
                return getattr(self, f'_v_{verb.lower()}')(object=object, options=options)
            except TypeError as err:
                logger.error(str(err))
                return 'Syntax error:\n' + self._usage(verb)
            except AttributeError as err:
                logger.error(str(err))
                return f'Unknown command "{verb}". Type "help" for list of commands.'
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

    def _usage_remove(self):
        return ['remove {context number}']

    def _usage_save(self):
        return [
            'save {filepath}',
            'save {filepath} {format=json|txt}'
        ]

    def _v_align(self, object: str, options: list):
        """Align objects within the gazetteer."""
        if object == 'self':
            return self.manager.align_self(options)
        else:
            return self.manager.align_external(object, options)

    def _v_contents(self):
        """List contents of the gazetteer."""
        return self.manager.contents()

    def _v_del(self, object: str, options: list):
        """See "remove"."""
        return self._v_remove(object, options)

    def _v_delete(self, object: str, options: list):
        """See "remove"."""
        return self._v_remove(object, options)

    def _v_drop(self):
        """Erase contents of the gazetteer from memory."""
        return self.manager.drop()
    
    def _v_examine(self, object: str, options: list):
        """Examine a single gazetteer object from the most recent "contents" listing."""
        if options:
            raise TypeError(options)
        return self.manager.examine(object)

    def _v_exit(self):
        """See "quit"."""
        self._v_quit()


    def _v_find(self, object: str, options: list):
        """Search the gazetteer for matching character strings."""
        if options:
            targets = [object,]
            targets.extend(options)
            return self.manager.find(targets)
        else:
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
        """See "contents"."""
        return self._v_contents()

    def _v_ls(self):
        """See "contents"."""
        return self._v_contents()

    def _v_merge(self, object:str, options: list):
        """Merge two or more items in the gazetteer."""
        context_numbers = [object]
        context_numbers.extend(options)
        return self.manager.merge(context_numbers)

    def _v_new(self, object: str, options: list=[]):
        """Create a new object in the gazetteer."""
        return self.manager.new(type_name=object, data=options)

    def _v_promote(self, object: str, options: list):
        """Turn a gazetteer object into a Place."""
        m = rx_integer_range.match(object)
        if m is not None:
            start = int(m.group('start'))
            end = int(m.group('end'))
            context_numbers = list(range(start, end + 1))
            context_numbers = [str(n) for n in context_numbers]
        else:
            m = rx_integer.match(object)
            if m is not None:
                context_numbers = [object]
        context_numbers = set(context_numbers)
        for opt in options:
            m = rx_integer.match(opt)
            if m is not None:
                context_numbers.add(opt)
        context_numbers = list(context_numbers)
        return self.manager.promote(context_numbers)

    def _v_remove(self, object: str, options: list):
        """Delete a single gazetteer object."""
        if options:
            raise TypeError(options)
        return self.manager.remove(object)

    def _v_review(self, object:str, options: list):
        """Review alignment matches for possible action."""
        fn = f'review_{object}'
        if options:
            fn += f'_{"_".join(options)}'
        return getattr(self.manager, fn)()

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
        """See "quit"."""
        self._v_quit()

    def _v_quit(self):
        """Quit interactive interface."""
        exit()

        
