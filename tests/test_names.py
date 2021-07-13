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
        assert_equal('moontown', n.id)
        assert_true(list(n.prior_ids)[0].startswith('Name.'))

    def test_init_romanized(self):
        n = Name(romanized=['Moontown', 'Mōntown'])
        assert_equal(['Moontown', 'Mōntown'], n.romanized)
        assert_equal('moontown', n.id)

    def test_init_cleanup(self):
        n = Name(romanized=['    Moontown'])
        assert_equal(['Moontown'], n.romanized)
        assert_equal('moontown', n.id)

    def test_init_cleanup_false(self):
        n = Name(romanized=['    Moontown'], cleanup=False)
        assert_equal(['    Moontown'], n.romanized)

    def test_init_attested(self):
        n = Name(
            attested='Moontown',
            romanized={'Moontown'})
        assert_equal('Moontown', n.attested)
        assert_equal(['Moontown'], n.romanized)
        assert_equal('moontown', n.id)

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

    def test_id_generation(self):
        n = Name(romanized='Moontown')
        assert_equal('moontown', n.id)
        n.romanized = 'Mù ēn dūn'
        assert_equal(n.id, 'moontown')  # uses alphabetically first romanized form if no attested
        n.attested='穆恩敦'
        assert_equal(n.id, 'mu-en-dun')  # attested overrides romanized
        prior = sorted(list(n.prior_ids))
        assert_equal(2, len(prior))
        assert_true(prior[0].startswith('Name.'))
        assert_equal('moontown', prior[1])
        




