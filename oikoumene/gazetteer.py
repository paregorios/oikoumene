#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gazetteer
"""

from copy import deepcopy
import logging
from oikoumene.indexing import StringIndex
from oikoumene.parsing import *
from oikoumene.place import Dict2PlaceParser, Place
from oikoumene.serialization import Serializeable
from oikoumene.stringlike import Dict2StringlikeParser, GeographicName, GeographicString
from typing import Union, Sequence
from types import FunctionType
from inspect import getmembers

logger = logging.getLogger(__name__)

class Gazetteer(Serializeable):
    """A collection of Place, GeographicName, and GeographicString objects"""

    def __init__(self, objs: Union[Sequence[Union[dict, Place, GeographicName, GeographicString]], dict, Place, GeographicName, GeographicString]=None):
        self._supported = (dict, Place, GeographicName, GeographicString)
        self.contents = {}
        self._indexes = {
            '_all_text': StringIndex()
        }
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
        else:
            obj.make_unique_id(list(self.contents.keys()))
            self.contents[obj.id] = obj
        self.reindex(obj.id)

    def get(self, criteria: dict=[], operator: str='and'):
        results = dict()
        for k, v in criteria.items():
            results[k] = getattr(self, f'_get_{k}')(v)
        if len(results) < len(criteria) and operator ==  'and':
            return {}
        ids = None
        for k, v in results.items():
            if ids is None:
                ids = set(v)
            elif operator == 'and':
                ids.intersection(v)
            elif operator == 'or':
                ids.union(v)
            else:
                raise NotImplementedError(operator)
        entries = dict()
        for id in ids:
            entries[id] = self.contents[id]
        return entries

    def _get_id(self, ids):
        return [id for id in ids if id in self.contents.keys()]

    def _get_text(self, values):
        return self._indexes['_all_text'].get(values, operator='or')

    def make_place(self, ids: list):
        if isinstance(ids, list):
            real_ids = ids
        elif isinstance(ids, str):
            real_ids = [ids,]
        else:
            raise TypeError(type(ids))
        for id in real_ids:
            target = Place()
            obj = self.contents[id]
            target = getattr(self, f'_merge_{type(obj).__name__.lower()}_to_place')(target, obj)
            self.add(target)
            self.remove(id)

    def merge(self, ids: list):
        if isinstance(ids, str):
            return self.contents[ids]
        elif isinstance(ids, list):
            pass
        else:
            raise TypeError(type(ids))
        objs = [self.contents[id] for id in ids]
        type_names = list(set([type(o).__name__ for o in objs]))
        target_type = None
        if 'Place' in type_names or len(type_names) > 1:
            target_type = 'Place'
        elif len(type_names) == 1 and type_names[0] in ['GeographicName', 'GeographicString']:
            rset = set(objs[0].romanized)
            for o in objs[1:]:
                rset.intersection(o.romanized)
            if len(rset) > 0:
                target_type = type_names[0]
            else:
                target_type = 'Place'
        else:
            raise NotImplementedError(type_names)
        _class = globals()[target_type]
        try:
            target = _class()
        except ValueError as err:
            if 'At least one romanized or attested name form must be provided to initialize' in str(err):
                target = objs[0]
                objs = objs[1:]
            else:
                raise
        for obj in objs:
            target = getattr(self, f'_merge_{type(obj).__name__.lower()}_to_{target_type.lower()}')(target, obj)
        self.add(target)
        for id in ids:
            self.remove(id)

    def _merge_geographicname_to_geographicname(self, target, gname):
        if gname.attested and target.attested:
            if gname.attested != target.attested:
                raise RuntimeError(
                    f'Cannot merge GeographicNames with differing attested forms '
                    f'({target.attested} vs. {gname.attested}')
        elif target.attested and not gname.attested:
            pass
        elif not target.attested and gname.attested:
            target.attested = gname.attested
        else:
            raise RuntimeError("?")
        for rname in gname.romanized:
            target.romanized = rname
        return target

    def _merge_geographicname_to_place(self, target, gname):
        target.add(gname)
        return target

    def _merge_geographicstring_to_place(self, target, gstring):
        target.add(gstring)
        return target

    def reindex(self, ids: list):
        if isinstance(ids, list):
            real_ids = ids
        elif isinstance(ids, str):
            real_ids = [ids,]
        else:
            raise TypeError(type(ids))
        for id in real_ids:
            try:
                obj = self.contents[id]
            except KeyError:
                raise ValueError(id)
            self._reindex_this(obj, id)

    def _reindex_this(self, obj, id):
        if isinstance(obj, str):
            self._indexes['_all_text'].add(obj, id)
        elif isinstance(obj, list):
            for o in obj:
                self._reindex_this(o, id)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                self._reindex_this(v, id)
        elif isinstance(obj, (GeographicName, GeographicString, Place)):
            for k, v in self._get_indexable_fields(obj).items():
                self._reindex_this(v, id)
        else:
            raise TypeError(type(obj))

    def _get_indexable_fields(self, obj):
        disallowed = {
            name for name, value in getmembers(type(obj)) 
                if isinstance(value, FunctionType)}
        disallowed.update(['id', 'prior_ids'])
        fields = [
            name for name in dir(obj) 
                if name[0] != '_' and name not in disallowed and hasattr(obj, name)]
        fields = {name: getattr(obj, name) for name in fields if getattr(obj, name)}
        return fields

    def remove(self, id:str):
        try:
            self.contents[id]
        except KeyError:
            return
        else:
            self.contents.pop(id)
            self._unindex(id)

    def _unindex(self, id):
        self._indexes['_all_text'].drop(id)

    def __str__(self):
        msg = []
        for id, data in self.contents.items():
            if isinstance(data, Place):
                msg.append(str(data))
            else:
                msg.append(f'{type(data).__name__}: {str(data)}')
        return '\n'.join(msg)



