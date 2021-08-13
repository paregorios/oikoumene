#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Line Interface
"""

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
        if not verb and not object:
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
            return getattr(self, f'_{verb.lower()}')(object=object, options=options)

    def _load(self, object: str, options: list):
        format = ''
        if options:
            if len(options) == 1:
                format=options[0]
            else:
                raise NotImplementedError(options)            
        else:
            format = object.split('.')[-1]
        return self.manager.load(object, format)


        
