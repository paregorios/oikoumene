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

class Test_StringIndex_Fuzzy(TestCase):

    def setUp(self):
        si = StringIndex()
        si.add('big cats', 'a')
        si.add('big cat', 'b')
        si.add('big dog', 'c')
        si.add('small cats', 'd')
        si.add('strange cats', 'e')
        si.add('strange brew', 'f')
        si.add('strange orange cats of doom', 'g')
        si.add('strange pink dogs of doom', 'h')
        si.add('strange orange cats of zoom', 'i')
        si.add('blades of glory', 'j')
        si.add('excess of cats displaying extreme attitudinality', 'k')
        si.add('big brats', 'l')
        si.add('small slats', 'm')
        si.add('big bats', 'n')
        si.add('big bandanas', 'o')
        si.add('biggish yellow road grater', 'p')
        self.si = si

    def test_get_phrase_fuzzy(self):
        r = self.si._get_phrase_fuzzy('orange cats of doom')
        r.sort()
        assert_equal(['g', 'i'], r)

    def test_get_phrases_fuzzy(self):
        sought = ['of cats', 'strange cats']
        r = self.si._get_phrases(sought, fuzzy=True)
        r.sort()
        assert_equal(['a', 'e', 'g', 'i', 'k'], r)

    def test_get_fuzzy_phrases(self):
        sought = ['of cats', 'strange cats']
        r = self.si.get(sought, indexes=['phrase'], fuzzy=True)
        r.sort()
        assert_equal(['a', 'e', 'g', 'i', 'k'], r)

    def test_substring_fuzzy(self):
        r = self.si._get_substring_fuzzy('braids')
        r.sort()
        assert_equal(['c', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'n', 'o', 'p'], r)

    def test_get_substrings_fuzzy(self):
        sought = ['zro', 'pbt']
        r = self.si._get_substrings(sought, fuzzy=True)
        r.sort()
        assert_equal(['f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'o', 'p'], r)

    def test_get_fuzzy_substrings(self):
        sought = ['zro', 'pbt']
        r = self.si.get(sought, indexes=['substring'], fuzzy=True)
        r.sort()
        assert_equal(['f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'o', 'p'], r)

    def test_get_value_fuzzy(self):
        r = self.si._get_value_fuzzy('big cat')
        r.sort()
        assert_equal(['a', 'b', 'l', 'n', 'o'], r)

    def test_get_values_fuzzy(self):
        sought = ['big cat', 'small cat']
        r = self.si._get_values(sought, fuzzy=True)
        r.sort()
        assert_equal(['a', 'b', 'd', 'l', 'm', 'n', 'o'], r)

    def test_get_fuzzy_values(self):
        sought = ['big cat', 'small cat']
        r = self.si.get(sought, indexes=['value'], fuzzy=True)
        r.sort()
        assert_equal(['a', 'b', 'd', 'l', 'm', 'n', 'o'], r)

    def test_get_word_fuzzy(self):
        r = self.si._get_word_fuzzy('priggish')
        assert_equal(['p'], r)

    def test_get_words_fuzzy(self):
        sought = ['priggish', 'rat']
        r = self.si._get_words(sought, fuzzy=True)
        r.sort()
        assert_equal(['l', 'p'], r)

    def test_get_fuzzy_words(self):
        sought = ['priggish', 'rat']
        r = self.si.get(sought, indexes=['word'], fuzzy=True)
        r.sort()
        assert_equal(['l', 'p'], r)

    def test_get_fuzzy_combo(self):
        sought = ['big', 'cat']
        indexes = ['value', 'phrase', 'word']
        r = self.si.get(sought, indexes=indexes, operator='or', fuzzy=True)
        r.sort()
        assert_equal(['a', 'b', 'c', 'd', 'e', 'g', 'i', 'k', 'l', 'n', 'o', 'p'], r)






