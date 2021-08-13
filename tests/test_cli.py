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


class Test_CLI_Init(TestCase):

    def setUp(self):
        self.cli = CLI()

    def tearDown(self):
        """Change me"""
        pass

    def test_help(self):
        cmd = 'help'
        r = self.cli._parse([cmd,])
        assert_true('contents: ' in r)

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

class Test_CLI_Verbs(TestCase):

    def setUp(self):
        self.cli = CLI()
        path = test_data_path / 'moontown_names.json'
        self.cli._v_load(str(path), ['json'])

    def tearDown(self):
        """Change me"""
        pass

    def test_contents(self):
        cmd = 'contents'
        r = self.cli._parse([cmd,])
        assert_equal("""1: 3 M5
2: Berry Road
3: Berry Road
4: Bob Hunt Road
5: Cedar Mountain
6: Chestnut Knob
7: Flint River
8: Hambrick Branch
9: Landing Strip
10: Lickskillet
11: Madison County Sky Park
12: Minnow Creek
13: Moontown
14: Moontown Airport
15: Moontown Road
16: North Alabama Canoe and Kayak
17: Sublett Bluff
18: Sublett Cemetery
19: The Mountain
20: The Saddle""",
            r)

    def test_find(self):
        cmd = 'find moontown'
        r = self.cli._parse(cmd.split())
        assert_equal("""1: Moontown
2: Moontown Airport
3: Moontown Road""",
            r)
