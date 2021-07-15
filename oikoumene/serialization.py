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

class OikoumeneJSONEncoder(json.JSONEncoder):
    """                                                                         
    Use __json__ attr or callable of object for JSON serialization.       
    https://stackoverflow.com/questions/38250765/extending-jsonencoder-to-call-json-for-serialization      
    """                                                                         

    def default(self, o):
        if hasattr(o, '_ddict'):
            if callable(o._ddict):
                return o._ddict()
            else:
                return o._ddict
        return super(OikoumeneJSONEncoder, self).default(o)


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
        try:
            j = json.dumps(self, cls=OikoumeneJSONEncoder, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, **kwargs)
        except TypeError:
            logger.error(pformat(self.__dict__, indent=4))  # sic
            raise 
        return j
            
class Serializeable(SerializeJSON):

    def __init__(self):
        SerializeJSON.__init__(self)

    def _ddict(self):
        d = {'object_type': type(self).__name__}
        field_names = [n for n in dir(self) if not n.startswith('_') and not isinstance(getattr(self, n), (MethodType))]
        for n in field_names:
            v = getattr(self, n)
            if isinstance(v, set):
                v = list(v)
            d[n] = v
        return d



            

        