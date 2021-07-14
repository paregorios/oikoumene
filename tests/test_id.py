#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ID utilities"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.id import make_id_valid, validate_id
from pathlib import Path
from unittest import TestCase
from uuid import uuid4

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_ValidateID(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_valid_uuid4(self):
        id = type(self).__name__ + str(uuid4())
        assert_true(validate_id(id))

    def test_valid_ascii(self):
        id = 'moontown'
        assert_true(validate_id(id))

    def test_valid_hyphenated(self):
        id = 'moontown-airport'
        assert_true(validate_id(id))

    def test_valid_oneup(self):
        id = 'moontown-airport.1'
        assert_true(validate_id(id))

    def test_invalid_normalization(self):
        id = 'moontown    airport    '
        assert_false(validate_id(id))

    def test_invalid_whitespace(self):
        id = 'moontown airport'
        assert_false(validate_id(id))

    def test_invalid_initial(self):
        id = '7moontown'
        assert_false(validate_id(id))

    def test_invalid_colon_initial(self):
        id = ':moontown'
        assert_false(validate_id(id))

class Test_MakeIDValid(TestCase):

    def test_already_valid(self):
        id = 'moontown'
        assert_equal(id, make_id_valid(id))

    def test_trailing_whitespace(self):
        id = 'moontown    '
        assert_equal('moontown', make_id_valid(id))

    def test_internal_whitespace(self):
        id = 'moontown airport'
        assert_equal('moontown-airport', make_id_valid(id))

    def test_bad_start(self):
        id = '3M5'
        assert_equal('_3M5', make_id_valid(id))

    def test_colon(self):
        id = 'moontown:3M5'
        assert_equal('moontown.3M5', make_id_valid(id))