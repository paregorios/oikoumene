#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test connection module"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.connection import Connection, VocabularyLookupError
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


class Test_Connection(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_connection(self):
        c = Connection()
        c.term = 'closeMatch'

    @raises(VocabularyLookupError)
    def test_connection_invalid(self):
        c = Connection()
        c.term = 'ludicrousMatch'
