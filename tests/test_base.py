#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base module tests"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.base import Base
from oikoumene.stringlike import GeographicString
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


class Test_Base(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_init(self):
        b = Base()

    def test_unique_id(self):
        b = Base()
        b.id = 'moontown'
        assert_equal('moontown', b.id)
        existing_ids = ['moontown']
        bb = Base()
        bb.id = 'moontown'
        bb.make_unique_id(existing_ids)
        assert_equal('moontown.1', bb.id)

    def test_unique_ids(self):
        b = Base()
        b.id = 'moontown'
        assert_equal('moontown', b.id)
        existing_ids = ['moontown', 'moontown.1', 'moontown-airport', 'hambrick-branch']
        b.make_unique_id(existing_ids)
        assert_equal('moontown.2', b.id)
