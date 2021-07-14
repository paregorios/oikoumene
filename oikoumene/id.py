#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDs
"""

import logging
import re
from oikoumene.normalization import norm

logger = logging.getLogger(__name__)

# NameStartChar ::= ":" | [A-Z] | "_" | [a-z] | [#xC0-#xD6] | [#xD8-#xF6] | [#xF8-#x2FF] | [#x370-#x37D] | [#x37F-#x1FFF] | [#x200C-#x200D] | [#x2070-#x218F] | [#x2C00-#x2FEF] | [#x3001-#xD7FF] | [#xF900-#xFDCF] | [#xFDF0-#xFFFD] | [#x10000-#xEFFFF]
# https://www.w3.org/TR/xml11/#NT-NameStartChar
NameStartChar = [
    ":",
    "[A-Z]",
    "_",
    "[a-z]",
    "[\u00C0-\u00D6]",
    "[\u00D8-\u00F6]",
    "[\u00F8-\u02FF]",
    "[\u0370-\u037D]",
    "[\u037F-\u1FFF]",
    "[\u200C-\u200D]",
    "[\u2070-\u218F]",
    "[\u2C00-\u2FEF]",
    "[\u3001-\uD7FF]",
    "[\uF900-\uFDCF]",
    "[\uFDF0-\uFFFD]",
    "[\U00010000-\U000EFFFF]"
]
# NCNameStartChar ::= NameStartChar - ':'
# https://www.w3.org/TR/xml-names11/#NT-NCNameStartChar
NCNameStartChar = NameStartChar.copy()
NCNameStartChar.remove(':')
NCNameStartChar = '|'.join(NCNameStartChar)
rx_NCNameStartChar = re.compile(f'({NCNameStartChar})')
    
# NameChar ::= NameStartChar | "-" | "." | [0-9] | #xB7 | [#x0300-#x036F] | [#x203F-#x2040]
# https://www.w3.org/TR/xml11/#NT-NameChar
NameChar = NameStartChar.copy()
NameChar.extend([r'\-', r'\.', '[0-9]', '\u00B7', '[\u0300-\u036F]', '[\u203F-\u2040]'])

# NCNameChar ::= NameChar - ':'
NCNameChar = NameChar.copy()
NCNameChar.remove(':')
NCNameChar = '|'.join(NCNameChar)
rx_NCNameChar = re.compile(f'^({NCNameChar})$')
rx_NCNameChars = re.compile(f'^({NCNameChar})*$')

# NCName ::= NCNameStartChar NCNameChar*
# https://www.w3.org/TR/xml-names11/#NT-NCName
NCName = f'({NCNameStartChar})({NCNameChar})*'
rx_NCName = re.compile(f'^{NCName}$')

rx_whitespace = re.compile(r'[\s\n]+')

def validate_id(value):
    """Ensure value conforms to W3C rules for xml:id plus oikoumene-specific restrictions."""

    # Attribute Value Normalization on IDs (Non-Normative)
    # https://www.w3.org/TR/xml-id/#id-avn
    # Attributes of type ID are subject to additional normalization rules: removing leading and trailing space characters and replacing sequences of spaces with a single space
    if value != norm(value):
        return False
    
    # the author of oikoumene has no interest in whitespace in ids
    if rx_whitespace.search(value) is not None:
        return False

    if value == '':
        return False
    
    # The normalized value of the attribute is an NCName according to the _Namespaces in XML Recommendation_
    # https://www.w3.org/TR/xml-id/#processing
    if rx_NCName.match(value) is None:
        return False

    return True

def make_id_valid(value):
    if validate_id(value):
        return value

    val = norm(value)
    if validate_id(val):
        return val

    val = val.replace(' ', '-')
    if validate_id(val):
        return val

    if val == '':
        raise ValueError(
            f'IDs cannot be zero-length strings, following normalization. Original value '
            f'"{value}" normalizes to "{val}".')

    if rx_NCNameStartChar.match(val[0]) is None:
        val = '_' + val
    if validate_id(val):
        return val

    if rx_NCNameChars.match(val[1:]) is None:
        revised = val[0]
        for v in val[1:]:
            if rx_NCNameChar.match(v) is None:
                revised += '.'
            else:
                revised += v
        val = revised

    if validate_id(val):
        return val

    

    
