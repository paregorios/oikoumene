#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indexing
"""

from itertools import combinations
import logging
from oikoumene.normalization import norm
from pprint import pprint

logger = logging.getLogger(__name__)

class StringIndex:

    def __init__(self):
        self.values = {}
        self.phrases = {}
        self.words = {}
        self.substrings = {}
        self.reverse = {}

    def add(self, value: str, ids: list):
        if not isinstance(value, str):
            raise TypeError(type(value))
        real_value = norm(value).lower()
        if isinstance(ids, str):
            real_ids = [ids,]
        elif isinstance(ids, list):
            real_ids = ids
        else:
            raise TypeError(type(ids))
        self._add_value(real_value, real_ids)
        self._add_phrases(real_value, real_ids)
        self._add_words(real_value, real_ids)
        self._add_substrings(real_value, real_ids)

    def _add_rev(self, ids, idx, value):
        for id in ids:
            try:
                self.reverse[id]
            except KeyError:
                self.reverse[id] = {}
            try:
                self.reverse[id][idx]
            except KeyError:
                self.reverse[id][idx] = set()
            self.reverse[id][idx].add(value)

    def _add_value(self, value, ids):
        try:
            self.values[value]
        except KeyError:
            self.values[value] = set()
        self.values[value].update(ids)
        self._add_rev(ids, 'values', value)

    def _add_words(self, value, ids):   
        words = value.split()
        for word in words:
            try:
                self.words[word]
            except KeyError:
                self.words[word] = set()
            self.words[word].update(ids)
            self._add_rev(ids, 'words', word)

    def _add_phrases(self, value, ids):
        words = value.split()
        for start, end in combinations(range(len(words)), 2):
            phrase = ' '.join(words[start:end+1])
            try:
                self.phrases[phrase]
            except KeyError:
                self.phrases[phrase] = set()
            self.phrases[phrase].update(ids)
            self._add_rev(ids, 'phrases', phrase)

    def _add_substrings(self, value, ids):
        chars = list(value)
        for start, end in combinations(range(len(chars)), 2):
            substring = ''.join(chars[start:end+1])
            try:
                self.substrings[substring]
            except KeyError:
                self.substrings[substring] = set()
            self.substrings[substring].update(ids)
            self._add_rev(ids, 'substrings', substring)

    def drop(self, ids: list):
        if isinstance(ids, list):
            real_ids = ids
        elif isinstance(ids, str):
            real_ids = [ids,]
        else:
            raise TypeError(type(ids))
        for id in real_ids:
            for idx_name, values in self.reverse[id].items():
                idx = getattr(self, idx_name)
                for value in values:
                    idx[value].remove(id)
                    if len(idx[value]) == 0:
                        idx.pop(value)

    def get(self, values: list, indexes: list=['value', 'word', 'phrase', 'substring'], operator: str='and'):
        if isinstance(values, str):
            real_values = [values,]
        elif isinstance(values, list):
            real_values = values
        else:
            raise TypeError(type(values))
        results = {}
        for idx in indexes:
            r = getattr(self, f'_get_{idx}s')(real_values, operator)
            if r:
                results[idx] = r
        if len(results) != len(indexes) and operator == 'and':
            return []
        matches = None
        for idx, ids in results.items():
            if matches is None:
                matches = set(ids)
            elif operator == 'and':
                matches = matches.intersection(ids)
            elif operator == 'or':
                matches.update(ids)
            else:
                raise ValueError(operator)
        return list(matches)

    def _get_phrase(self, phrase):
        try:
            result = self.phrases[phrase]
        except KeyError:
            return []
        else:
            return list(result)

    def _get_phrases(self, phrases: list, operator: str='and'):
        return self._get_multiples('phrase', phrases, operator)

    def _get_substring(self, substring):
        try:
            result = self.substrings[substring]
        except KeyError:
            return []
        else:
            return list(result)

    def _get_substrings(self, substrings: list, operator: str='and'):
        return self._get_multiples('substring', substrings, operator)

    def _get_value(self, value):
        try:
            result = self.values[value]
        except KeyError:
            return []
        else:
            return list(result)

    def _get_values(self, values: list, operator: str='and'):
        return self._get_multiples('value', values, operator)

    def _get_word(self, word):
        try:
            result = self.words[word]
        except KeyError:
            return []
        else:
            return list(result)

    def _get_words(self, words: list, operator: str='and'):
        return self._get_multiples('word', words, operator)

    def _get_multiples(self, index: str, values: list, operator: str='and'):
        results = {}
        for value in values:
            r = getattr(self, f'_get_{index}')(value)
            if r:
                results[value] = r
        if len(values) != len(results) and operator == 'and':
            return []
        matches = None
        for value, ids in results.items():
            if matches is None:
                matches = set(ids)
            elif operator == 'and':
                matches = matches.intersection(ids)
            elif operator == 'or':
                matches.update(ids)
        if matches is None:
            return []
        return list(matches)