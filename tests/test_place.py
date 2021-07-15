#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Places"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.stringlike import GeographicName, GeographicString
from oikoumene.place import Place
from pathlib import Path
from pprint import pprint
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

    @raises(TypeError)
    def test_init(self):
        p = Place()

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