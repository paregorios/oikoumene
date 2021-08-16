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
from oikoumene.place import Place
from pathlib import Path
from pprint import pformat, pprint
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

    def test_stringlike_dicts(self):
        path = Path('data/examples/moontown_names.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        assert_equal(20, len(gaz.contents))
        ids = {make_id_valid(slugify(d['attested'])): d['attested'] for d in j}
        for id, v in ids.items():
            assert_equal(v, gaz.contents[id].attested)

    def test_place_dicts(self):
        path = Path('data/examples/moontown_places.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        assert_equal(15, len(gaz.contents))
        names = []
        strings = []
        for pid, place in gaz.contents.items():
            names.extend([name.attested for nid, name in place.names.items()])
            strings.extend([string.attested for sid, string in place.strings.items()])
        assert_equal(17, len(names))
        assert_equal(3, len(strings))
        sought = []
        for o in j:
            for k in ['name', 'names', 'string', 'strings']:
                vals = None
                try:
                    vals = o['name']
                except KeyError:
                    continue
                if isinstance(vals, str):
                    sought.append(vals)
                elif isinstance(vals, list):
                    sought.extend(vals)
                else:
                    raise RuntimeError()
        sought = set(sought)
        values = names + strings
        values = set(values)
        assert_false(sought.difference(values))

    def test_str(self):
        path = Path('data/examples/moontown_places.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        gaz_string = str(gaz)
        sought = []
        for pid, place in gaz.contents.items():
            sought.extend([name.attested for nid, name in place.names.items()])
            sought.extend([string.attested for sid, string in place.strings.items()])
        sought = list(set(sought))
        for s in sought:
            assert_true(s in gaz_string)

    def test_get(self):
        path = Path('data/examples/moontown_names.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        entries = gaz.get({'id': ['chestnut-knob']})
        assert_equal(1, len(entries))
        entries = gaz.get({'text': ['moon']})
        assert_equal(3, len(entries))

    def test_remove(self):
        path = Path('data/examples/moontown_names.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        assert_equal(20, len(gaz.contents))
        entries = gaz.get({'id': ['chestnut-knob']})
        assert_equal(1, len(entries))
        gaz.remove('chestnut-knob')
        assert_equal(19, len(gaz.contents))
        entries = gaz.get({'id': ['chestnut-knob']})
        assert_equal(0, len(entries))

    def test_merge(self):
        path = Path('data/examples/moontown_names.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        assert_equal(20, len(gaz.contents))
        merge_ids = ['_3-m5', 'landing-strip', 'madison-county-sky-park', 'moontown-airport']
        gaz.merge(merge_ids)
        assert_equal(17, len(gaz.contents))
        misses = 0
        for id in merge_ids:
            try:
                gaz.contents[id]
            except KeyError:
                misses += 1
        assert_equal(4, misses)
        entries = gaz.get({'text': ['sky', 'strip', 'airport', '3 M5']})
        assert_equal(1, len(entries))
        for id, obj in entries.items():
            assert_true(isinstance(obj, Place))
            print(obj.json())

    def test_make_place(self):
        path = Path('data/examples/moontown_names.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        merge_ids = ['_3-m5', 'landing-strip', 'madison-county-sky-park', 'moontown-airport']
        gaz.merge(merge_ids)
        entries = gaz.get({'text': ['berry']})
        merge_ids = list(entries.keys())
        gaz.merge(merge_ids)
        gaz.make_place([id for id, obj in gaz.contents.items() if not isinstance(obj, Place)])
        assert_equal(16, len(gaz.contents))
        for id, obj in gaz.contents.items():
            assert_true(isinstance(obj, Place))
        assert_equal(20, len(gaz._indexes['_all_text'].values))
        
        

