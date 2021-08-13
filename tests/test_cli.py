#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test CLI module"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.cli import CLI
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


class Test_CLI(TestCase):

    def setUp(self):
        self.cli = CLI()

    def tearDown(self):
        """Change me"""
        pass

    def test_load(self):
        path = test_data_path / 'strings.txt'
        cmd = f'load {path}'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Read 5 objects from '))
        assert_true(r.endswith('oikoumene/tests/data/strings.txt.'))
        assert_equal(5, len(self.cli.manager.gaz.contents))
        cmd = f'drop'
        r = self.cli._parse(cmd.split())
        assert_equal('Erased current gazetteer from memory (5 objects).', r)
        path = test_data_path / 'moontown_names.json'
        cmd = f'load {path}'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Read 20 objects from '))
        assert_true(r.endswith('oikoumene/tests/data/moontown_names.json.'))
        assert_equal(20, len(self.cli.manager.gaz.contents))
