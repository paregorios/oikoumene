#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test CLI module"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from oikoumene.cli import CLI
from pathlib import Path
import shlex
from unittest import TestCase

TestCase.maxDiff = None

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
        path = test_data_path / 'foo.json'
        path.unlink(missing_ok=True)
        path = test_data_path / 'foo.txt'
        path.unlink(missing_ok=True)
        self.cli = CLI()
        path = test_data_path / 'moontown_names.json'
        self.cli._v_load(str(path), ['json'])

    def tearDown(self):
        """Change me"""
        pass

    def test_contents(self):
        cmd = 'contents'
        r = self.cli._parse([cmd,])
        assert_equal("""1: 3 M5 [GeographicName]
2: Berry Road [GeographicName]
3: Berry Road [GeographicName]
4: Bob Hunt Road [GeographicName]
5: Cedar Mountain [GeographicName]
6: Chestnut Knob [GeographicName]
7: Flint River [GeographicName]
8: Hambrick Branch [GeographicName]
9: Landing Strip [GeographicString]
10: Lickskillet [GeographicName]
11: Madison County Sky Park [GeographicName]
12: Minnow Creek [GeographicName]
13: Moontown [GeographicName]
14: Moontown Airport [GeographicName]
15: Moontown Road [GeographicName]
16: North Alabama Canoe and Kayak [GeographicName]
17: Sublett Bluff [GeographicName]
18: Sublett Cemetery [GeographicName]
19: The Mountain [GeographicName]
20: The Saddle [GeographicName]""",
            r)

    def test_examine(self):
        cmd = 'ls'
        self.cli._parse(cmd.split())
        cmd = 'examine'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Syntax error'))
        cmd = 'examine 1'
        r = self.cli._parse(cmd.split())
        assert_true(
            r.startswith('3 M5\n{'))
        cmd = 'examine 1 noodle'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Syntax error'))

    def test_examine_numeric(self):
        cmd = 'ls'
        self.cli._parse(cmd.split())
        cmd = '1'
        r = self.cli._parse(cmd.split())
        assert_true(
            r.startswith('3 M5\n{'))
        cmd = '999'
        r = self.cli._parse(cmd.split())
        assert_equal(
            'Context number out of range (999). Valid numbers are currently from 1 to 20.',
            r)

    def test_find(self):
        cmd = 'find moontown'
        r = self.cli._parse(cmd.split())
        assert_equal("""1: Moontown [GeographicName]
2: Moontown Airport [GeographicName]
3: Moontown Road [GeographicName]""",
            r)

    def test_json(self):
        cmd = 'json'
        r = self.cli._parse([cmd])
        assert_true('"object_type": "Gazetteer"' in r)

    def test_len(self):
        cmd = 'len'
        r = self.cli._parse([cmd])
        assert_equal('There are 20 objects in the gazetteer.', r)
        
    def test_save(self):
        path = test_data_path / 'foo.json'
        assert_false(path.exists())
        cmd = f'save {path}'
        r = self.cli._parse(cmd.split())
        assert_true(path.exists())
        path = test_data_path / 'foo.txt'
        assert_false(path.exists())
        cmd = f'save {path}'
        r = self.cli._parse(cmd.split())
        assert_true(path.exists())

    def test_parse_unknown_verb(self):
        cmd = 'banana'
        r = self.cli._parse(cmd.split())
        assert_equal(
            'Unknown command "banana". Type "help" for list of commands.',
            r)
        cmd = 'banana jr.'
        r = self.cli._parse(cmd.split())
        assert_equal(
            'Unknown command "banana". Type "help" for list of commands.',
            r)

    def test_parse_extraneous_object(self):
        cmd = 'drop basket'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Syntax error'))

    def test_parse_missing_object(self):
        cmd = 'remove'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Syntax error'))

    def test_parse_lost_context(self):
        cmd = 'remove 999'
        r = self.cli._parse(cmd.split())
        assert_equal(
            'Context has been lost. Execute "contents" or "find" to refresh.',
            r)

    def test_parse_invalid_context(self):
        cmd = 'ls'
        r = self.cli._parse(cmd.split())
        cmd = 'remove 999'
        r = self.cli._parse(cmd.split())
        assert_equal(
            'Context number out of range (999). Valid numbers are currently from 1 to 20.',
            r)

class Test_CLI_Destructive(TestCase):

    def setUp(self):
        path = test_data_path / 'foo.json'
        path.unlink(missing_ok=True)
        path = test_data_path / 'foo.txt'
        path.unlink(missing_ok=True)
        self.cli = CLI()
        path = test_data_path / 'moontown_names.json'
        self.cli._v_load(str(path), ['json'])

    def test_new_place(self):
        cmd = "new place"
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Created Place with id='))

    def test_new_name(self):
        cmd = "new name attested:Moontown"
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Created GeographicName with id='))

    def test_new_string(self):
        cmd = "new string romanized:'Landing Strip'"
        r = self.cli._parse(shlex.split(cmd))
        assert_true(r.startswith('Created GeographicString with id='))

    def test_remove(self):
        cmd = 'ls'
        self.cli._parse(cmd.split())
        cmd = 'remove'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Syntax error'))
        cmd = 'remove 1'
        r = self.cli._parse(cmd.split())
        assert_equal('Removed "3 M5" object from the gazetteer.', r)
        cmd = 'remove 1 fish'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Syntax error'))
        cmd = 'ls'
        self.cli._parse(cmd.split())
        cmd = 'del 1'
        r = self.cli._parse(cmd.split())
        assert_equal('Removed "Berry Road" object from the gazetteer.', r)
        cmd = 'ls'
        self.cli._parse(cmd.split())
        cmd = 'delete 1'
        r = self.cli._parse(cmd.split())
        assert_equal('Removed "Berry Road" object from the gazetteer.', r)

    def test_merge(self):
        cmd = 'find airport sky'
        self.cli._parse(cmd.split())
        cmd = 'merge 1 2'
        r = self.cli._parse(cmd.split())
        assert_true(r.startswith('Merged 2 objects to new object'))

    def test_promote(self):
        cmd = 'find hambrick'
        self.cli._parse(cmd.split())
        cmd = 'promote 1'
        r = self.cli._parse(cmd.split())
        assert_equal('Promoted 1 to Place(s).', r)
        cmd = 'ls'
        self.cli._parse(cmd.split())
        cmd = 'promote 1 2 4'
        r = self.cli._parse(cmd.split())
        assert_equal('Promoted 3 to Place(s).', r)
        cmd = 'ls'
        self.cli._parse(cmd.split())
        cmd = 'promote 1-10'
        r = self.cli._parse(cmd.split())
        assert_equal('Promoted 10 to Place(s).', r)
        cmd = 'ls'
        r = self.cli._parse(cmd.split())
        assert_equal("""1: 3 M5 [Place]
2: Berry Road [Place]
3: Berry Road [Place]
4: Bob Hunt Road [Place]
5: Cedar Mountain [Place]
6: Chestnut Knob [Place]
7: Flint River [Place]
8: Hambrick Branch [Place]
9: Landing Strip [Place]
10: Lickskillet [Place]
11: Madison County Sky Park [GeographicName]
12: Minnow Creek [GeographicName]
13: Moontown [GeographicName]
14: Moontown Airport [GeographicName]
15: Moontown Road [GeographicName]
16: North Alabama Canoe and Kayak [GeographicName]
17: Sublett Bluff [GeographicName]
18: Sublett Cemetery [GeographicName]
19: The Mountain [GeographicName]
20: The Saddle [GeographicName]""",
            r)