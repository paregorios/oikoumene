#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEst indexing"""

from oikoumene.indexing import StringIndex
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from pprint import pprint
from pathlib import Path
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_StringIndex(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_value(self):
        si = StringIndex()
        si._add_value('big cat', ['Fielder'])
        r = si._get_value('big cat')
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])

    def test_words(self):
        si = StringIndex()
        si._add_words('big cat', ['Fielder'])
        r = si._get_word('big')
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])
        r = si._get_words(['cat', 'big'])
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])

    def test_phrase(self):
        si = StringIndex()
        si._add_phrases('the big cat is staring at me', ['Fielder'])
        r = si._get_phrase('cat is staring')
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])
        r = si._get_phrases(['big cat', 'staring at'])
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])

    def test_substring(self):
        si = StringIndex()
        si._add_substrings('the big cat is staring at me', ['Fielder'])
        r = si._get_substring('g ca')
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])
        r = si._get_substrings(['g ca', 'ring'])
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])

    def test_add(self):
        si = StringIndex()
        si.add('the big cat is staring at me', 'Fielder')  # sic
        r = si.get(['big cat'], operator='or')
        assert_equal(1, len(r))
        assert_equal('Fielder', r[0])
