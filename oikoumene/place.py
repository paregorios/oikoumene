#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Place
"""

import logging
from oikoumene.parsing import DictParser
from oikoumene.stringlike import GeographicName, GeographicString
from pprint import pprint
from typing import Sequence, Type, Union

logger = logging.getLogger(__name__)

from oikoumene.base import Base
from oikoumene.serialization import Serializeable

class Place(Base, Serializeable):

    def __init__(self, source):
        Base.__init__(self)
        Serializeable.__init__(self)
        self.parser2gs = DictParser(GeographicString)
        self.parser2gn = DictParser(GeographicName)
        self.names = {}
        self.strings = {}
        self.parse(source)

    def parse(self, source: Union[dict, GeographicName, GeographicString, Sequence[Union[dict, GeographicName, GeographicString]]]):
        if not isinstance(source, (dict, GeographicName, GeographicString, Sequence)):
            raise TypeError(
                f'Unexpected type ({type(source)}) passed to Place "add" method. '
                f'Expected one or a {Sequence} of {dict}, {GeographicName}, {GeographicString}.')
        if isinstance(source, (list, tuple)):
            for item in source:
                self.add(item)
        else:
            self.add(source)

    def _parse_dict(self, d: dict) -> Union[GeographicName, GeographicString]:
        if not isinstance(d, dict):
            raise TypeError(
                f'Unexpected type ({type(d)}) passed to Place "_parse_dict" method. '
                f'Expected {dict}')
        try:
            object_type = d['object_type']
        except KeyError:
            object_type = 'GeographicString'
        if object_type == 'GeographicName':
            od = self.parser2gn.parse(d)
        else:
            od = self.parser2gs.parse(d)
        if len(od) != 1:
            raise RuntimeError('egad')
        for k, v in od.items():
            return v
                    
    def add(self, obj:Union[dict, GeographicName, GeographicString]):
        if not isinstance(obj, (dict, GeographicName, GeographicString)):
            raise TypeError(
                f'Unexpected type ({type(obj)}) passed to Place "add" method. '
                f'Expected {GeographicName} or {GeographicString}')
        if isinstance(obj, dict):
            this_obj = self._parse_dict(obj)
        else:
            this_obj = obj
        if isinstance(this_obj, GeographicName):
            self.add_name(this_obj)
        elif isinstance(this_obj, GeographicString):
            self.add_string(this_obj)

    def add_name(self, obj:GeographicName):
        if not isinstance(obj, GeographicName):
            raise TypeError(
                f'Unexpected type ({type(obj)}) passed to Place "add_name" method. '
                f'Expected {GeographicName}.')
        try:
            self.names[obj.id]
        except KeyError:
            self.names[obj.id] = obj
        else:
            new_id = obj.make_unique_id(list(self.names.keys()))
            self.names[new_id] = obj
        
    def add_string(self, obj:GeographicString):
        if not isinstance(obj, GeographicString):
            raise TypeError(
                f'Unexpected type ({type(obj)}) passed to Place "add_string" method. '
                f'Expected {GeographicString}.')
        try:
            self.strings[obj.id]
        except KeyError:
            self.strings[obj.id] = obj
        else:
            new_id = obj.make_unique_id(list(self.strings.keys()))
            self.strings[new_id] = obj
