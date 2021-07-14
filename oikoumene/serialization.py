#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serialization Mixins
"""

import json
import logging
from pprint import pformat
from types import MethodType

logger = logging.getLogger(__name__)


class SerializeJSON:

    def __init__(self):
        pass

    def json(
        self,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        **kwargs
    ):
        d = {
            'object_type': type(self).__name__
        }
        field_names = [n for n in dir(self) if not n.startswith('_') and not isinstance(getattr(self, n), MethodType)]
        for n in field_names:
            v = getattr(self, n)
            if isinstance(v, set):
                v = list(v)
            d[n] = v
        try:
            j = json.dumps(d, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, **kwargs)
        except TypeError:
            logger.error(pformat(d, indent=4))
            raise 
        return j
            
class Serializeable(SerializeJSON):

    def __init__(self):
        SerializeJSON.__init__(self)

            

        