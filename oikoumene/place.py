#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Place
"""

from copy import deepcopy
import logging
from oikoumene.base import Base
from oikoumene.serialization import Serializeable
from oikoumene.stringlike import Dict2StringlikeParser, GeographicName, GeographicString
from pprint import pprint
from typing import Sequence, Type, Union

logger = logging.getLogger(__name__)


class Place(Base, Serializeable):

    def __init__(self, source=None, encoding='utf-8'):
        Base.__init__(self)
        Serializeable.__init__(self)
        self.names = {}
        self.strings = {}
        self._dict_parser = Dict2StringlikeParser()
        if source is not None:
            self.add(source, encoding=encoding)

    def add(
        self, 
        source: Union[dict, GeographicName, GeographicString, Sequence[Union[dict, GeographicName, GeographicString]]],
        encoding='utf-8'
    ):
        if isinstance(source, str):
            result = GeographicString(attested=source)
        elif isinstance(source, bytes):
            s = source.decode(encoding)
            result = GeographicString(attested=s)
        elif isinstance(source, (list, tuple)):
            for obj in source:
                self.add(obj)
            return
        elif isinstance(source, Sequence):
            raise NotImplementedError(type(source))
        elif isinstance(source, dict):
            result = self._dict_parser.parse_dict(source)
        elif isinstance(source, (GeographicName, GeographicString)):
            result = source
        else:
            raise TypeError(
                f'Unexpected type ({type(source)}) passed to Place "add" method. '
                f'Expected {dict}, {GeographicName}, {GeographicString} or a {Sequence} of same.')            

        if isinstance(result, GeographicName):
            self.add_name(result)
        elif isinstance(result, GeographicString):
            self.add_string(result)

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

class Dict2PlaceParser:
    """
    Convert a dictionary to a Place
    
    Methods
    -------

    parse_dict()
        Perform dictionary conversion.

    """

    def __init__(self):
        self._stringlike_parser = Dict2StringlikeParser()

    def parse_dict(self, source: dict) -> Place:
        """
        Perform dictionary conversion.
        
        Arguments
        ---------

        source: dict
            A python dictionary in which each key-value pair corresponds to desired attribute names and
            associated values. Specifically supported values include "attested" and "romanized", and at least
            one non-zero-length value must be provided for one of these two keys. Note, however, that all 
            key-value pairs are passed on to __init__() method of the output class. The special key
            "object_type" may be included in the dictionary to indicate the desired class of the resulting
            object. If "object_type" is omitted from the dictionary, or if its value is a zero-length,
            the parser will default to creating a GeographicString. See also the "object_type" keyword
            argument to this function, which may be used to override this behavior.

        """
        if not isinstance(source, dict):
            raise TypeError(
                f'Unexpected type ({type(source)}) passed as "source" argument to "parse_dict" method. '
                f'Expected {dict}.')
        p = Place()
        for k in ['name', 'names', 'string', 'strings', 'attested', 'romanized']:
            try:
                v = source[k]
            except KeyError:
                continue
            else:
                if k in ['name', 'names']:
                    object_type = 'GeographicName'
                else:
                    object_type = 'GeographicString'
                if k in ['attested', 'romanized']: 
                    field_name = k
                else:
                    field_name = 'attested'
                if isinstance(v, (str, dict)):
                    self._parse_item(object_type, field_name, v, p)
                elif isinstance(v, (list, tuple)):
                    self._parse_sequence(object_type, field_name, v, p)
                else:
                    raise TypeError(type(v))
        return p

    def _parse_sequence(self, object_type, field_name, values, place):
        for v in values:
            self._parse_item(object_type, field_name, v, place)

    def _parse_item(self, object_type, field_name, value, place):
        if isinstance(value, str):
            d = {
                'object_type': object_type,
                field_name: value}
        elif isinstance(value, dict):
            d = deepcopy(value)
            d['object_type'] = object_type
        place.add(d)


