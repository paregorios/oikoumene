#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base mixin
"""

from oikoumene.id import make_id_valid
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

class Base:
    """Base Mixin Class"""
    def __init__(self):
        self._id = '.'.join((type(self).__name__, str(uuid4())))

    def make_unique_id(self, existing_ids: list):
        id = self.id
        if len(set(existing_ids).intersection([id])) == 1:
            similar = [i for i in existing_ids if i == id or i.startswith(f'{id}.')]
            new_id = f'{id}.{len(similar)}'
            self.id = new_id
            return new_id
        return id

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        if not isinstance(value, str):
            raise TypeError(
                f'Invalid type ({type(value)}) used to set "id". Expected {str}.')
        valid_id = make_id_valid(value)
        try:
            self.prior_ids
        except AttributeError:
            self.prior_ids = set()
        self.prior_ids.add(self._id)
        self._id = valid_id





