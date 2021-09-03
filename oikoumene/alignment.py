#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alignment to external gazetteers
"""

from enum import unique
from geopy.geocoders import get_geocoder_for_service
from geopy.extra.rate_limiter import RateLimiter
import logging
from oikoumene.gazetteer import Gazetteer
from oikoumene.normalization import norm
from slugify import slugify
from time import sleep

logger = logging.getLogger(__name__)

class BaseAligner:

    def __init__(self, gaz: Gazetteer, operator: str='and', **kwargs):
        self.gaz = gaz
        self.operator = operator
        self.criteria = {}
        for k, v in kwargs.items():
            self.criteria[k] = v

    def align_object(self, obj):
        return None

    def _get_unique_strings(self, obj):
        unique_strings = set()
        for fieldname, values in self.gaz._get_indexable_fields(obj).items():
            if isinstance(values, str):
                unique_strings.add(norm(values))
            elif isinstance(values, list):
                unique_strings.update([norm(v) for v in values])
        return list(unique_strings)

class SelfAligner(BaseAligner):

    def __init__(self, **kwargs):
        BaseAligner.__init__(self, **kwargs)

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

    def _align_text(self, obj, **options):
        unique_strings = self._get_unique_strings(obj)
        try:
            fuzzy = options['fuzzy']
        except KeyError:
            fuzzy = False
        results = self.gaz._indexes['_all_text'].get(unique_strings, indexes=['value'], operator='or', fuzzy=fuzzy)
        return [r for r in results if r != obj.id]

class ExternalAligner(BaseAligner):

    def __init__(self, geocoder='Nominatim', **kwargs):
        BaseAligner.__init__(self, **kwargs)
        cls = get_geocoder_for_service(geocoder)
        self.geocoder_name = geocoder
        self.sleep_period = 9999
        self.sleep_duration = 0
        self.api_calls = 0
        if geocoder == 'Nominatim':
            self.sleep_period = 5
            self.sleep_duration = 1.5
        self.geolocator = cls(
            user_agent='Oikoumene/0.1 (+https://github.com/paregorios/oikoumene)',
            timeout=3)
        self.match_cache = {}

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

    def _align_text(self, obj, **options):
        unique_strings = self._get_unique_strings(obj)
        try:
            s = options['postfix']
        except KeyError:
            pass
        else:
            unique_strings = [us + f', {s}' for us in unique_strings]
        results = set()
        geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1, max_retries=1, error_wait_seconds=5, return_value_on_exception=-1)
        for us in unique_strings:
            if self.api_calls > 0 and self.api_calls % self.sleep_period == 0:
                if self.sleep_duration > 0:
                    duration = int(self.api_calls/self.sleep_period) * self.sleep_duration
                    print(f'Sleeping for {duration} seconds to avoid overtaxing the {self.geocoder_name} API.')
                    sleep(duration)                    
            print(f'>>> Searching for "{us}" at {self.geocoder_name}')
            prior_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.FATAL)  # geopy RateLimiter is noisy on logging.WARNING
            matches = geocode(us, exactly_one=False)
            logging.getLogger().setLevel(prior_level)
            self.api_calls += 1
            if matches is None:
                qty = 0
            elif matches == -1:
                qty = 'TIMEOUT ERROR ON QUERY'
                matches = None
            else:
                qty = len(matches)
            print(f'<<< {self.geocoder_name} results: {qty}')
            if matches is not None:
                for match in matches:
                    id = self._make_id(match)
                    self.match_cache[id] = match
                    results.add(id)
        return list(results)

    def _make_id(self, location):
        formulae = {
            'Nominatim': ['const:osm', 'copy:osm_type', 'str:osm_id']
        }
        try:
            formula = formulae[self.geocoder_name]
        except KeyError:
            raise NotImplementedError(self.geocoder_name)
        id = ''
        for criterion in formula:
            k, v = criterion.split(':')
            if id:
                id += '-'
            if k == 'const':
                id += v
            elif k == 'copy':
                id += location.raw[v]
            elif k == 'str':
                id += str(location.raw[v])
            else:
                raise RuntimeError(k)
        return id

