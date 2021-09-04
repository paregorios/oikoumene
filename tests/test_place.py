#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Places"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.connection import Connection
from oikoumene.id import make_id_valid
from oikoumene.stringlike import GeographicName, GeographicString
from oikoumene.place import Dict2PlaceParser, Place
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


class Test_Place(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_init(self):
        p = Place()

    @raises(TypeError)
    def test_init_bad(self):
        p = Place(7)

    def test_init_string(self):
        p = Place('Moontown')

    def test_init_bytes(self):
        p = Place(b'Moontown', encoding='ascii')

    @raises(NotImplementedError)
    def test_init_bytearray(self):
        b = bytearray('Moontown', encoding='ascii')
        p = Place(b, encoding='ascii')

    @raises(NotImplementedError)
    def test_init_range(self):
        r = range(7)
        p = Place(r)

    def test_init_dict(self):
        d = {
            'object_type': 'GeographicName',
            'attested': 'Moontown'}
        p = Place(d)
        assert_equal(1, len(p.names))
        assert_equal('Moontown', p.names['moontown'].romanized[0])

    def test_init_dict_notype(self):
        # if object_type is not specified, we get a GeographicString
        d = {'attested': 'landing strip'}
        p = Place(d)
        assert_equal(1, len(p.strings))
        assert_equal('landing strip', p.strings['landing-strip'].romanized[0])

    def test_init_geoname(self):
        n = GeographicName(attested='Moontown', romanized='Moontown')
        p = Place(n)
        assert_equal(1, len(p.names))
        assert_equal('Moontown', p.names['moontown'].romanized[0])

    def test_init_geostring(self):
        s = GeographicString(attested='Moontown', romanized='Moontown')
        p = Place(s)
        assert_equal(1, len(p.strings))
        assert_equal('Moontown', p.strings['moontown'].romanized[0])

    def test_init_sequence(self):
        seq = [
            {'object_type': 'GeographicName', 'attested': 'Moontown Airport'},
            GeographicName(attested='Madison County Skypark', romanized='Madison County Skypark'),
            {'object_type': 'GeographicString', 'attested': '3M5'},
            GeographicString(attested='landing strip', romanized='landing strip'),
        ]
        p = Place(seq)
        assert_equal(2, len(p.names))
        assert_equal(2, len(p.strings))
        for k in ['moontown-airport', 'madison-county-skypark']:
            assert_true(k in p.names.keys())
        for k in ['_3m5', 'landing-strip']:
            assert_true(k in p.strings.keys())

    def test_add_connection(self):
        c = Connection(term='closeMatch')
        p = Place()
        p.add_connection(c)
        assert_equal(1, len(p.connections))

    def test_add_name(self):
        n = GeographicName('Moontown')
        p = Place()
        p.add_name(n)
        assert_equal(1, len(p.names))
        assert_equal('Moontown', p.names['moontown'].attested)

    @raises(TypeError)
    def test_add_name_bad(self):
        s = GeographicString('Moontown')  # sic
        p = Place()
        p.add_name(s)

    def test_add_string(self):
        s = GeographicString('Moontown')
        p = Place()
        p.add_string(s)
        assert_equal(1, len(p.strings))
        assert_equal('Moontown', p.strings['moontown'].attested)

    @raises(TypeError)
    def test_add_string_bad(self):
        n = GeographicName('Moontown')  # sic
        p = Place()
        p.add_string(n)

    def test_add_id_collision(self):
        nn = [
            GeographicName('Moontown'),
            GeographicName('Moontown')]
        p = Place(nn)
        p.names['moontown']
        p.names['moontown.1']
        ss = [
            GeographicString('landing strip'),
            GeographicString('landing strip')]
        p.add(ss)
        p.strings['landing-strip']
        p.strings['landing-strip.1']

class Test_Dict2PlaceParser(TestCase):

    def setUp(self):
        self.d2p = Dict2PlaceParser()

    def test_init(self):
        pass

    @raises(TypeError)
    def test_parse_bad(self):
        self.d2p.parse_dict(7)

    @raises(TypeError)
    def test_parse_bad_subordinate(self):
        self.d2p.parse_dict({'name': 7})

    def test_parse_str_attested(self):
        p = self.d2p.parse_dict({'attested': 'Moontown'})
        assert_equal(1, len(p.strings))
        assert_equal('Moontown', p.strings['moontown'].attested)

    def test_parse_str_romanized(self):
        p = self.d2p.parse_dict({'romanized': 'Moontown'})
        assert_equal(1, len(p.strings))
        assert_equal('Moontown', p.strings['moontown'].romanized[0])

    def test_parse_list_attested(self):
        strings = ['3M5', 'landing strip', 'Moontown Airport']
        p = self.d2p.parse_dict({'attested': strings})
        assert_equal(3, len(p.strings))
        for s in strings:
            id = make_id_valid(slugify(s))
            assert_equal(s, p.strings[id].attested)

    def test_parse_various(self):
        strings = ['landing strip', '3M5']
        d = {
            'names': 'Moontown Airport',
            'strings': strings}
        p = self.d2p.parse_dict(d)
        assert_equal(1, len(p.names))
        assert_equal(2, len(p.strings))
        assert_equal('Moontown Airport', p.names['moontown-airport'].attested)
        for s in strings:
            id = make_id_valid(slugify(s))
            assert_equal(s, p.strings[id].attested)
        
    def test_parse_complex(self):
        names = [
            {'attested': 'Moontown Airport', 'romanized': 'Moontown Airport'},
            {'attested': 'فرودگاه مونتاون', 'romanized': ['frwdgh mwntwn', 'frudgah muntaun', 'frūdgāh mūntāūn']}
        ]
        strings = [
            {'attested': 'landing strip', 'romanized': 'landing strip'},
            {'attested': '3M5', 'romanized': '3M5'}]
        d = {
            'names': names,
            'strings': strings}
        p = self.d2p.parse_dict(d)
        assert_equal(2, len(p.names))
        assert_equal(2, len(p.strings))
        for n in names:
            id = make_id_valid(slugify(n['attested']))
            assert_equal(n['attested'], p.names[id].attested)
        assert_equal('Moontown Airport', p.names['moontown-airport'].attested)
        for s in strings:
            id = make_id_valid(slugify(s['attested']))
            assert_equal(s['attested'], p.strings[id].attested)
        assert_equal(3, len(p.names['frwdgh-mwntwn'].romanized))
