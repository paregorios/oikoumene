#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python 3 tests template (changeme)"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.parsing import StringParser
from oikoumene.stringlike import norm
from pathlib import Path
from slugify import slugify
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


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
