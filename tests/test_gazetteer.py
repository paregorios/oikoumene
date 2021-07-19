#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Gazetteer module"""

from copy import deepcopy
import json
import logging
from oikoumene.id import make_id_valid
from oikoumene.stringlike import GeographicString
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.gazetteer import Gazetteer
from oikoumene.parsing import StringParser
from pathlib import Path
from pprint import pprint
from slugify import slugify
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_Gazetteer(TestCase):

    def setUp(self):
        parser = StringParser(output_fieldname='romanized')
        s = 'Moontown, Cedar Mountain, Chestnut Knob, Hambrick Branch, Moontown Airport'
        self.geostrings = parser.parse(s)

    def tearDown(self):
        """Change me"""
        pass

    def test_init(self):
        g = Gazetteer()

    def test_init_dict(self):
        g = Gazetteer(self.geostrings)
        assert_equal(5, len(g.contents))

    @raises(TypeError)
    def test_init_dict_bad(self):
        gd = deepcopy(self.geostrings)
        gd['chickn'] = 7
        g = Gazetteer(gd)

    def test_init_list(self):
        geolist = [o for id, o in self.geostrings.items()]
        g = Gazetteer(geolist)
        assert_equal(5, len(g.contents))

    @raises(TypeError)
    def test_init_list_bad(self):
        geolist = [o for id, o in self.geostrings.items()]
        geolist.append(7)
        g = Gazetteer(geolist)

    def test_init_singleton(self):
        gs = self.geostrings['moontown']
        g = Gazetteer(gs)
        assert_equal(1, len(g.contents))

    @raises(TypeError)
    def test_init_singleton_bad(self):
        g = Gazetteer(7)

    def test_add(self):
        g = Gazetteer(self.geostrings)
        gs = GeographicString(romanized='Moontown Road')
        g.add(gs)
        assert_equal(6, len(g.contents))

    @raises(TypeError)
    def test_add_bad(self):
        g = Gazetteer(self.geostrings)
        g.add(7)

    def test_add_doublet(self):
        g = Gazetteer(self.geostrings)
        gs = GeographicString(romanized='Moontown')
        g.add(gs)
        assert_equal(6, len(g.contents))

    def test_json(self):
        g = Gazetteer(self.geostrings)
        j = g.json()

    def test_stringlike_dict(self):
        path = Path('data/examples/moontown_names.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        assert_equal(20, len(gaz.contents))
        ids = {make_id_valid(slugify(d['attested'])): d['attested'] for d in j}
        for id, v in ids.items():
            assert_equal(v, gaz.contents[id].attested) 
            


