#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base mixin
"""

import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

class Base:
    """Base Mixin Class"""
    def __init__(self):
        self._id = '.'.join((type(self).__name__, str(uuid4())))


