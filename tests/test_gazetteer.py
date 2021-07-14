#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Gazetteer module"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.gazetteer import Gazetteer
from oikoumene.parsing import StringParser
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


class Test_Gazetteer(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_init(self):
        parser = StringParser(output_fieldname='romanized', delimiter='\n')
        path = test_data_path / 'strings.txt'
        geostrings = parser.parse(path, encoding='ascii')
        g = Gazetteer(geostrings)
        assert_equal(5, len(g.contents))


