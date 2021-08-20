#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test aligment module"""

import json
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.alignment import SelfAligner
from oikoumene.gazetteer import Gazetteer
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


class Test_SelfAligner(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_doublet(self):
        path = Path('data/examples/moontown_names.json').resolve()
        with open(path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        gaz = Gazetteer(j)
        entries = gaz.get({'text': ['berry']})
        assert_equal(2, len(entries))
        ids = list(entries.keys())
        candidate = gaz.contents[ids[0]]
        sa = SelfAligner(gaz, text={})
        matches = sa.align_object(candidate)
        assert_equal(1, len(matches))
        assert_equal(ids[1], matches[0])
