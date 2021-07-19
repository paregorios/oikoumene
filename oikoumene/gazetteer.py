#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gazetteer
"""

import logging
from oikoumene.parsing import *
from oikoumene.place import Dict2PlaceParser, Place
from oikoumene.serialization import Serializeable
from oikoumene.stringlike import Dict2StringlikeParser, GeographicName, GeographicString
from typing import Union, Sequence

logger = logging.getLogger(__name__)

class Gazetteer(Serializeable):
    """A collection of Place, GeographicName, and GeographicString objects"""

    def __init__(self, objs: Union[Sequence[Union[dict, Place, GeographicName, GeographicString]], dict, Place, GeographicName, GeographicString]=None):
        self._supported = (dict, Place, GeographicName, GeographicString)
        self.contents = {}
        self._dict_parser = Dict2StringlikeParser()
        self._place_parser = Dict2PlaceParser()
        if objs is None:
            return
        fail = tuple()
        if isinstance(objs, (list, tuple)):
            for o in objs:
                if not isinstance(o, self._supported):
                    fail = o
                    break
                elif isinstance(o, dict):
                    try:
                        parsed = self._dict_parser.parse_dict(o)
                    except ValueError:
                        parsed = self._place_parser.parse_dict(o)
                    self.add(parsed)
                else:
                    self.add(o)
        elif isinstance(objs, dict):
            for id, o in objs.items():
                if isinstance(o, self._supported):
                    self.add(o)
                else:
                    fail = o
                    break
        elif isinstance(objs, (Place, GeographicName, GeographicString)):
            self.add(objs)
        else:
            raise TypeError(
                f'Unexpected type ({type(objs)}) passed to Gazetteer initialization. '
                f'Expected one or more of {Place}, {GeographicName}, {GeographicString}.')
        if fail:
            raise TypeError(
                f'Unexpected type ({type(fail)}) in {type(objs)} passed to Gazetteer initialization. '
                f'Expected one of ({self._supported}).')

    def add(self, obj: Union[Place, GeographicName, GeographicString]):
        if not isinstance(obj, (Place, GeographicName, GeographicString)):
            raise TypeError(
                f'Invalid type ({type(obj)}) passed to gazetteer "add" method. '
                f'Expected {GeographicName}, {GeographicString}, {Place}')
        try:
            self.contents[obj.id]
        except KeyError:
            self.contents[obj.id] = obj
            # index?
        else:
            obj.make_unique_id(list(self.contents.keys()))
            self.contents[obj.id] = obj

    def get(self, id: str):
        pass

    def remove(self, id:str):
        pass

    def __str__(self):
        msg = []
        for id, data in self.contents.items():
            if isinstance(data, Place):
                msg.append(str(data))
            else:
                msg.append(f'{type(data).__name__}: {str(data)}')
        return '\n'.join(msg)



