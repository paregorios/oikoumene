#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alignment to external gazetteers
"""

import logging
from oikoumene.gazetteer import Gazetteer
from oikoumene.normalization import norm
import urllib.parse

logger = logging.getLogger(__name__)

class BaseAligner:

    def __init__(self, operator: str='and', **kwargs):
        self.operator = operator
        self.criteria = {}
        for k, v in kwargs.items():
            self.criteria[k] = v

    def align_object(self, obj):
        matches = {}
        for criterion, options in self.criteria.items():
            try:
                matches[criterion] = getattr(self, f'_align_{criterion}')(obj, **options)
            except AttributeError:
                raise NotImplementedError(f'Unsupported alignment criterion for {type(self).__name__}: {criterion}')
        results = None
        for k, v in matches.items():
            if results is None:
                results = set(v)
            elif self.operator == 'and':
                results = results.intersection(v)
            elif self.operator == 'or':
                results = results.update(v)
            else:
                raise NotImplementedError(f'Unsupported operator "{self.operator}" for {type(self).__name__}')
        return list(results)

class SelfAligner(BaseAligner):

    def __init__(self, gaz: Gazetteer, **kwargs):
        self.gaz = gaz
        BaseAligner.__init__(self, **kwargs)

    def _align_text(self, obj, **options):
        
        unique_strings = set()
        for fieldname, values in self.gaz._get_indexable_fields(obj).items():
            if isinstance(values, str):
                unique_strings.add(values)
            elif isinstance(values, list):
                unique_strings.update([norm(v) for v in values])
        unique_strings = list(unique_strings)
        try:
            fuzzy = options['fuzzy']
        except KeyError:
            fuzzy = False
        results = self.gaz._indexes['_all_text'].get(unique_strings, indexes=['value'], operator='or', fuzzy=fuzzy)
        return [r for r in results if r != obj.id]

class OnlineAligner(BaseAligner):

    def __init__(self):
        BaseAligner.__init__(self)

class GeoNamesAligner(OnlineAligner):

    def __init__(self):
        OnlineAligner.__init__(self)
        self.base_uri = 'http://api.geonames.org/searchJSON?'

    def search(self, name: str):
        query = f'name={urllib.parse.quote(name)}&maxRows=10&username={self.username}'
        uri = self.base_uri + query
