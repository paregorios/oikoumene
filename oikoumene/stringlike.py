#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Names
"""

from collections.abc import Sequence, Set
import logging
from oikoumene.base import Base
from oikoumene.id import make_id_valid
from oikoumene.normalization import norm
from oikoumene.serialization import Serializeable
from pprint import pformat
from slugify import slugify
from typing import List, Union

logger = logging.getLogger(__name__)

class CitedString(Base, Serializeable):

    def __init__(
        self,
        attested: str='',
        romanized: Union[Sequence[str], Set[str]]=[],
        cleanup: bool=True,
        **kwargs
    ):
        Base.__init__(self)
        Serializeable.__init__(self)
        if not romanized:
            raise ValueError(
                f'At least one romanized name form must be provided to initialize a Name.')
        self._cleanup = cleanup
        self.attested = attested
        self.romanized = romanized
        for kw, arg in kwargs.items():
            setattr(self, kw, arg)

    # attested form of the string (i.e., appears in a witness)
    @property
    def attested(self) -> str:
        try:
            return self._attested
        except AttributeError:
            return ''

    @attested.setter
    def attested(self, value: str):
        if self._cleanup:
            val = norm(value)
            if val == '':
                return
        else:
            val = value
        try:
            prior_val = self._attested
        except AttributeError:
            prior_val = ''
        if val != prior_val:
            self._attested = val
            self._generate_id()

    # romanized form(s) of the attested string
    @property
    def romanized(self) -> List[str]:
        try:
            return self._romanized
        except AttributeError:
            return []

    @romanized.setter
    def romanized(self, values:Union[str, Sequence[str], Set[str]]):
        expected = (str, Sequence, Set)
        if not isinstance(values, expected):
            expected = ', '.join([str(e) for e in expected])
            raise TypeError(
                f'Invalid type used to set Name.romanized. '
                f'Expected {expected} but got {type(values)}.')
        if isinstance(values, str):
            values = [values]
        dirty = False
        for v in values:
            if not isinstance(v, str):
                raise TypeError(
                    f'Invalid type used to set Name.romanized. '
                    f'Expected {str} but got {type(v)} ({v}).')
            if self._cleanup:
                val = norm(v)
                if val == '':
                    continue
            else:
                val = v
            try:
                self._romanized
            except AttributeError:
                self._romanized = []
            name_set = set(self._romanized)
            name_set.add(val)
            name_set = sorted(list(name_set))
            if name_set != self._romanized:
                self._romanized = name_set
                dirty = True
        if dirty:
            self._generate_id()

    def _generate_id(self):
        """Make the most useful possible ID for this string."""
        base = self.attested
        if not base:
            base = self.romanized[0]
        slug = slugify(base)
        if slug != self.id:
            try:
                self.prior_ids
            except AttributeError:
                self.prior_ids = set()
            self.prior_ids.add(self.id)
            self.id = slug

class GeographicName(CitedString):
    """A Geographic Name"""

    def __init__(
        self,
        attested: str='',
        romanized: Union[Sequence[str], Set[str]]=[],
        cleanup: bool=True,
        **kwargs
    ):
        CitedString.__init__(self, attested, romanized, cleanup, **kwargs)


class GeographicString(CitedString):
    """A geographic string"""

    def __init__(
        self,
        attested: str='',
        romanized: Union[Sequence[str], Set[str]]=[],
        cleanup: bool=True,
        **kwargs
    ):
        CitedString.__init__(self, attested, romanized, cleanup, **kwargs)
        
