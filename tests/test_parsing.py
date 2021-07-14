#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python 3 tests template (changeme)"""

from io import StringIO
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.parsing import BaseParser, DictParser, StringParser
from oikoumene.stringlike import norm, GeographicString
from pathlib import Path
from pprint import pprint
from slugify import slugify
from unittest import TestCase

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass

class Test_BaseParser(TestCase):

    def test_unique_id(self):
        parser = BaseParser()
        existing_ids = ['moontown']
        gs = GeographicString(romanized='Moontown')
        assert_equal('moontown', gs.id)
        parser._unique_id(gs, existing_ids)
        assert_equal('moontown.1', gs.id)

    def test_unique_ids(self):
        parser = BaseParser()
        existing_ids = ['moontown', 'moontown.1', 'moontown-airport', 'hambrick-branch']
        gs = GeographicString(romanized='Moontown')
        assert_equal('moontown', gs.id)
        parser._unique_id(gs, existing_ids)
        assert_equal('moontown.2', gs.id)
        existing_ids.append(gs.id)
        gs = GeographicString(romanized='Minnow Creek')
        assert_equal('minnow-creek', gs.id)
        parser._unique_id(gs, existing_ids)
        assert_equal('minnow-creek', gs.id)
        existing_ids.append(gs.id)
        gs = GeographicString(romanized='Moontown')
        assert_equal('moontown', gs.id)
        parser._unique_id(gs, existing_ids)
        assert_equal('moontown.3', gs.id)

class Test_StringParser(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_init(self):
        parser = StringParser()

    def test_parse_string(self):
        parser = StringParser(output_fieldname='romanized')
        s = 'Moontown, Cedar Mountain, Chestnut Knob, Hambrick Branch, Moontown Airport'
        geostrings = parser.parse(s)
        assert_equal(5, len(geostrings))
        expected = {slugify(part): norm(part) for part in s.split(',')}
        for k, v in expected.items():
            assert_equal([v], geostrings[k].romanized)

    def test_parse_bytes(self):
        parser = StringParser(output_fieldname='romanized')
        s = 'Moontown, Cedar Mountain, Chestnut Knob, Hambrick Branch, Moontown Airport'
        b = s.encode(encoding='ascii')
        geostrings = parser.parse(b, encoding='ascii')
        assert_equal(5, len(geostrings))
        expected = {slugify(part): norm(part) for part in s.split(',')}
        for k, v in expected.items():
            assert_equal([v], geostrings[k].romanized)

    def test_parse_file(self):
        parser = StringParser(output_fieldname='romanized', delimiter='\n')
        path = test_data_path / 'strings.txt'
        geostrings = parser.parse(path, encoding='ascii')
        assert_equal(5, len(geostrings))
        expected = {
            'moontown': {'romanized': ['Moontown']},
            'cedar-mountain': {'romanized': ['Cedar Mountain']},
            'chestnut-knob': {'romanized': ['Chestnut Knob']},
            'hambrick-branch': {'romanized': ['Hambrick Branch']},
            'moontown-airport': {'romanized': ['Moontown Airport']}
        }
        for id, eg in expected.items():
            for fieldname, value in eg.items():
                assert_equal(value, getattr(geostrings[id], fieldname))

    def test_parse_textio(self):
        parser = StringParser(output_fieldname='romanized', delimiter='\n')
        s = 'Moontown, Cedar Mountain, Chestnut Knob, Hambrick Branch, Moontown Airport'
        s = s.replace(', ', '\n')
        source = StringIO(s)
        geostrings = parser.parse(source)
        assert_equal(5, len(geostrings))

    def test_parse_attested(self):
        parser = StringParser(output_fieldname='attested', delimiter='\n')
        path = test_data_path / 'strings.txt'
        geostrings = parser.parse(path, encoding='ascii')
        assert_equal(5, len(geostrings))
        expected = {
            'moontown': {'attested': 'Moontown', 'romanized': ['Moontown']},
            'cedar-mountain': {'attested': 'Cedar Mountain', 'romanized': ['Cedar Mountain']},
            'chestnut-knob': {'attested': 'Chestnut Knob', 'romanized': ['Chestnut Knob']},
            'hambrick-branch': {'attested': 'Hambrick Branch', 'romanized': ['Hambrick Branch']},
            'moontown-airport': {'attested': 'Moontown Airport', 'romanized': ['Moontown Airport']}
        }
        for id, eg in expected.items():
            for fieldname, value in eg.items():
                assert_equal(value, getattr(geostrings[id], fieldname))

    def test_parse_doublets(self):
        parser = StringParser(output_fieldname='romanized')
        s = 'Moontown, Moontown Airport, Moontown Road, Moontown'
        geostrings = parser.parse(s)
        assert_equal(4, len(geostrings))
        expected = ['moontown', 'moontown-airport', 'moontown-road', 'moontown.1']
        assert_equal(expected, sorted(list(geostrings.keys())))

    @raises(TypeError)
    def test_parse_bad(self):
        parser = StringParser()
        parser.parse(7)

class Test_DictParser(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_init(self):
        parser = DictParser()

    def test_parse_single(self):
        d = {'romanized': 'Moontown'}
        parser = DictParser()
        geostrings = parser.parse(d)
        assert_equal(1, len(geostrings))
        for id, gs in geostrings.items():
            assert_equal('moontown', id)
            assert_equal('moontown', gs.id)
            assert_equal(['Moontown'], gs.romanized)

    def test_parse_multiple(self):
        dd = [
            {'attested': 'Moontown'},
            {'attested': 'Cedar Mountain'},
            {'attested': 'Chestnut Knob'},
            {'attested': 'Hambrick Branch'},
            {'attested': 'Moontown Airport'}
        ]
        parser = DictParser()
        geostrings = parser.parse(dd)
        assert_equal(5, len(geostrings))
        expected = {}
        for d in dd:
            expected = {
                slugify(v): {
                    'attested': v,
                    'romanized': [slugify(v, lowercase=False, separator=' ')]
                } for k, v in d.items()}
        for id, egs in expected.items():
            for fieldname, value in egs.items():
                assert_equal(value, getattr(geostrings[id], fieldname))

    @raises(TypeError)
    def test_parse_bad(self):
        parser = DictParser()
        parser.parse(7)

    @raises(ValueError)
    def test_parse_noname(self):
        parser = DictParser()
        parser.parse({'fish': 'minnow'})
