#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test manager mondul"""

import json
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.gazetteer import Gazetteer
from oikoumene.manager import Manager
from pathlib import Path
from unittest import TestCase

TestCase.maxDiff = None

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_Manager(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_init(self):
        m = Manager()

    def test_load_txt(self):
        m = Manager()
        path = test_data_path / 'strings.txt'
        r = m.load(path, 'txt')
        assert_true(r.startswith('Read 5 objects from '))

    def test_load_json(self):
        m = Manager()
        path = test_data_path / 'moontown_names.json'
        r = m.load(path, 'json')
        assert_true(r.startswith('Read 20 objects from '))

    def test_len(self):
        m = Manager()
        path = test_data_path / 'moontown_names.json'
        r = m.load(path, 'json')
        assert_equal('There are 20 objects in the gazetteer.', m.len())

    def test_str(self):
        m = Manager()
        path = test_data_path / 'strings.txt'
        m.load(path, 'txt')
        r = m.str()
        assert_equal(
            """GeographicString: Moontown
GeographicString: Cedar Mountain
GeographicString: Chestnut Knob
GeographicString: Hambrick Branch
GeographicString: Moontown Airport""",
            r)

    def test_json(self):           
        m = Manager()
        path = test_data_path / 'strings.txt'
        m.load(path, 'txt')
        r = m.json()
        j = json.loads(r)
        assert_equal(5, len(j['contents']))

    def test_find(self):
        m = Manager()
        path = test_data_path / 'strings.txt'
        m.load(path, 'txt')
        r = m.find('Moontown')
        assert_equal("""1: Moontown [GeographicString]
2: Moontown Airport [GeographicString]""",
            r)

    def test_contents(self):
        m = Manager()
        path = test_data_path / 'strings.txt'
        m.load(path, 'txt')
        r = m.contents()
        assert_equal("""1: Cedar Mountain [GeographicString]
2: Chestnut Knob [GeographicString]
3: Hambrick Branch [GeographicString]
4: Moontown [GeographicString]
5: Moontown Airport [GeographicString]""",
            r)


class Test_Manager_Alignment(TestCase):

    def test_alignment_nominatim(self):
        m = Manager()
        m.load('data/examples/moontown_names.json')
        r = m.align_external('Nominatim', options=['Madison County, Alabama'])
        assert_equal(
            '15 objects in the gazetteer have possible matches with Nominatim objects. Use "review Nominatim matches" to merge matches selectively.',
            r)
        r = m.review_nominatim_matches()
        assert_true('Alignment candidate 1 of 15' in r)
        r = m.review_nominatim_matches()
        assert_true('Alignment candidate 2 of 15' in r)
