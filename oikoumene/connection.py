#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Connection
"""

import json
import logging
from oikoumene.base import Base
from oikoumene.serialization import Serializeable
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_PATH = Path('data/vocabularies/connection_types.json')

class VocabularyAware:

    def __init__(self, vocab):
        if isinstance(vocab, dict):
            self.vocab = vocab
        else:
            if isinstance(vocab, str):
                vocab_path = Path(vocab)
            elif isinstance(vocab, Path):
                vocab_path = vocab
            else:
                raise TypeError(type(vocab))
            with open(vocab_path, 'r', encoding='utf-8') as f:
                self.vocab = json.load(f)
            del f

class VocabularyLookupError(LookupError):
    """Report a vocabulary constraint error"""

    def __init__(self, vocab, term):
        self.vocab = vocab
        self.term = term
        self.message = (
            'Term "{}" not found in vocabulary. '
            'Valid values: [{}]'
            ''.format(
                term, ', '.join(sorted(vocab.keys()))))
        super().__init__(self.message)

class Connection(Base, Serializeable, VocabularyAware):

    def __init__(self, vocab=DEFAULT_PATH, context=None, target=None, term=None):
        Base.__init__(self)
        Serializeable.__init__(self)
        VocabularyAware.__init__(self, vocab)
        self._context = None
        self._target = None
        self._term = None
        if context:
            self.context = context
        if target:
            self.target = target
        if term:
            self.term = term

    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, value):
        try:
            self.vocab[value]
        except KeyError:
            raise VocabularyLookupError(self.vocab, value)
        else:
            self._term = value
    
    def get(self):
        return self._term

    
        