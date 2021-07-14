#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gazetteer
"""

import logging
from oikoumene.stringlike import GeographicName, GeographicString
from typing import Union, Sequence

logger = logging.getLogger(__name__)

class Place:

    def __init__(self):
        pass

class Gazetteer:
    """A collection of Place, GeographicName, and GeographicString objects"""

    def __init__(self, objs: Union[Sequence[Union[Place, GeographicName, GeographicString]], Place, GeographicName, GeographicString]=None):
        self.supported = (Place, GeographicName, GeographicString)
        self.contents = {}
        if objs is None:
            return
        fail = tuple()
        if isinstance(objs, (list, tuple)):
            items = {}
            for o in objs:
                if isinstance(o, self.supported):
                    items[o.id] = o
                else:
                    fail = o
                    break
        elif isinstance(objs, dict):
            items = {}
            for id, o in objs.items():
                if isinstance(o, self.supported):
                    items[id] = o
                else:
                    fail = o
                    break
        elif isinstance(objs, (Place, GeographicName, GeographicString)):
            items = {objs.id: objs}
        else:
            raise TypeError(
                f'Unexpected type ({type(objs)}) passed to Gazetteer initialization. '
                f'Expected one or more of {Place}, {GeographicName}, {GeographicString}.')
        if fail:
            raise TypeError(
                f'Unexpected type ({type(fail)}) in {type(objs)} passed to Gazetteer initialization. '
                f'Expected one of ({self.supported}).')
        for id, o in items.items():
            self.add(o)

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



