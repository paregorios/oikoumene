#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalization
"""

import logging
from textnorm import normalize_space, normalize_unicode

logger = logging.getLogger(__name__)

def norm(v):
    return normalize_unicode(normalize_space(v), 'NFC')
