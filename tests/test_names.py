#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test oikoumene/names module"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.names import Name
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


class Test_Name(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    @raises(ValueError)
    def test_init(self):
        n = Name()

    def test_init_reqs(self):
        n = Name(romanized=['Moontown'])
        assert_equal(['Moontown'], n.romanized)

    def test_init_romanized(self):
        n = Name(romanized=['Moontown', 'Mōntown'])
        assert_equal(['Moontown', 'Mōntown'], sorted(n.romanized))

    def test_init_cleanup(self):
        n = Name(romanized=['    Moontown'])
        assert_equal(['Moontown'], n.romanized)

    def test_init_cleanup_false(self):
        n = Name(romanized=['    Moontown'], cleanup=False)
        assert_equal(['    Moontown'], n.romanized)

    def test_init_attested(self):
        n = Name(
            attested='Moontown',
            romanized={'Moontown'})
        assert_equal('Moontown', n.attested)
        assert_equal(['Moontown'], n.romanized)

    def test_init_adhoc(self):
        n = Name(romanized=('Moontown',), banana='crispy')
        assert_equal('crispy', n.banana)

    def test_set_attested(self):
        n = Name(romanized=['Moontown'])
        n.attested = 'Moontown'
        assert_equal('Moontown', n.attested)
        assert_equal(['Moontown'], n.romanized)

    def test_set_romanized(self):
        n = Name(romanized=['Moontown'])
        n.romanized = ['Moontown', '   Moontown', '']
        assert_equal(['Moontown'], n.romanized)

    @raises(TypeError)
    def test_set_romanized_bad(self):
        n = Name(romanized='Moontown')
        n.romanized = 73

    @raises(TypeError)
    def test_set_romanized_bad_sequence(self):
        n = Name(romanized='Moontown')
        n.romanized = [73]



