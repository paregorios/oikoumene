#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test oikoumene.stringlike module"""

import json
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.stringlike import _CitedString, Dict2StringlikeParser, GeographicName, GeographicString
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


class Test_CitedString(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    @raises(ValueError)
    def test_init(self):
        n = _CitedString()

    def test_init_reqs(self):
        n = _CitedString(romanized=['Moontown'])
        assert_equal(['Moontown'], n.romanized)
        assert_equal('moontown', n.id)
        assert_true(list(n.prior_ids)[0].startswith('_CitedString.'))

    def test_init_romanized(self):
        n = _CitedString(romanized=['Moontown', 'Mōntown'])
        assert_equal(['Moontown', 'Mōntown'], n.romanized)
        assert_equal('moontown', n.id)

    def test_init_cleanup(self):
        n = _CitedString(romanized=['    Moontown'])
        assert_equal(['Moontown'], n.romanized)
        assert_equal('moontown', n.id)

    def test_init_cleanup_false(self):
        n = _CitedString(romanized=['    Moontown'], cleanup=False)
        assert_equal(['    Moontown'], n.romanized)

    def test_init_attested(self):
        n = _CitedString(attested='Moontown')
        assert_equal('Moontown', n.attested)
        assert_equal(['Moontown'], n.romanized)
        assert_equal('moontown', n.id)

    def test_init_both(self):
        n = _CitedString(
            attested='Moontown',
            romanized={'Moontown'})
        assert_equal('Moontown', n.attested)
        assert_equal(['Moontown'], n.romanized)
        assert_equal('moontown', n.id)

    def test_set_attested(self):
        n = _CitedString(romanized=['Moontown'])
        n.attested = 'Moontown'
        assert_equal('Moontown', n.attested)
        assert_equal(['Moontown'], n.romanized)

    def test_set_romanized(self):
        n = _CitedString(romanized=['Moontown'])
        n.romanized = ['Moontown', '   Moontown', '']
        assert_equal(['Moontown'], n.romanized)

    @raises(TypeError)
    def test_set_romanized_bad(self):
        n = _CitedString(romanized='Moontown')
        n.romanized = 73

    @raises(TypeError)
    def test_set_romanized_bad_sequence(self):
        n = _CitedString(romanized='Moontown')
        n.romanized = [73]

    def test_id_generation(self):
        n = _CitedString(romanized='Moontown')
        assert_equal('moontown', n.id)
        n.romanized = 'Mù ēn dūn'
        assert_equal(n.id, 'moontown')  # uses alphabetically first romanized form if no attested
        n.attested='穆恩敦'
        assert_equal(n.id, 'mu-en-dun')  # attested overrides romanized
        prior = sorted(list(n.prior_ids))
        assert_equal(2, len(prior))
        assert_true(prior[0].startswith('_CitedString.'))
        assert_equal('moontown', prior[1])

    def test_id_set(self):
        n = _CitedString(romanized='Moontown Airport')
        assert_equal('moontown-airport', n.id)
        n.id = '3M5'
        assert_equal('_3M5', n.id)

    @raises(ValueError)
    def test_id_set_empty(self):
        n = _CitedString(romanized='Moontown Airport')
        assert_equal('moontown-airport', n.id)
        n.id = '     '

    @raises(TypeError)
    def test_id_set_bad(self):
        n = _CitedString(romanized='Moontown Airport')
        assert_equal('moontown-airport', n.id)
        n.id = 12345

    def test_json(self):
        n = _CitedString(
            romanized='Moontown',
            attested='Moontown')
        j = n.json()
        d = json.loads(j)
        assert_equal(5, len(d))
        assert_equal(
            ['attested', 'id', 'object_type', 'prior_ids', 'romanized'],
            sorted(list(d.keys())))
        expected = {
            'attested': 'Moontown',
            'id': 'moontown',
            'object_type': '_CitedString',
            'romanized': ['Moontown']}
        for k, v in expected.items():
            assert_equal(v, d[k])
        assert_true(d['prior_ids'][0].startswith('_CitedString.'))

    def test_adhoc_field(self):
        n = _CitedString(
            romanized='Moontown',
            attested='Moontown',
            wikipedia='https://en.wikipedia.org/wiki/Moontown,_Alabama')
        assert_equal(['Moontown'], n.romanized)
        assert_equal('Moontown', n.attested)
        assert_equal('moontown', n.id)
        assert_equal('https://en.wikipedia.org/wiki/Moontown,_Alabama', n.wikipedia)


class Test_GeographicName(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    @raises(ValueError)
    def test_init(self):
        n = GeographicName()

class Test_GeographicString(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    @raises(ValueError)
    def test_init(self):
        n = GeographicString()

class Test_Dict2StringlikeParser(TestCase):

    def setUp(self):
        self.parser = Dict2StringlikeParser()

    @raises(TypeError)
    def test_bad_result_type(self):
        self.parser.parse_dict('foo')

    @raises(ValueError)
    def test_unsupported_object_type_type(self):
        self.parser.parse_dict({'romanized': 'foo', 'object_type': ['Airship', 'Submarine']})

    @raises(ValueError)
    def test_unsupported_object_type_value(self):
        self.parser.parse_dict({'romanized': 'foo', 'object_type': 'Airship'})

    @raises(TypeError)
    def test_bad_object_type_override_type(self):
        self.parser.parse_dict({'romanized': 'foo'}, object_type=7)

    @raises(ValueError)
    def test_bad_object_type_override_value(self):
        self.parser.parse_dict({'romanized': 'foo'}, object_type='Airship')

    @raises(ValueError)
    def test_nostrings(self):
        self.parser.parse_dict({})

    def test_default_object_type(self):
        o = self.parser.parse_dict({'romanized': 'landing strip'})
        assert_true(isinstance(o, GeographicString))
        assert_equal('landing-strip', o.id)
        assert_equal(['landing strip'], o.romanized)

    def test_geographic_string(self):
        d = {
            'romanized': 'landing strip',
            'object_type': 'GeographicString'
        }
        o = self.parser.parse_dict(d)
        assert_true(isinstance(o, GeographicString))
        assert_equal('landing-strip', o.id)
        assert_equal(['landing strip'], o.romanized)

    def test_geographic_name(self):
        d = {
            'romanized': 'Moontown Airport',
            'object_type': 'GeographicName'
        }
        o = self.parser.parse_dict(d)
        assert_true(isinstance(o, GeographicName))
        assert_equal('moontown-airport', o.id)
        assert_equal(['Moontown Airport'], o.romanized)
    

