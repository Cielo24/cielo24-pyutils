# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import random
import string


class RandomPasswordGenerator(object):
    uppercase_chars = string.uppercase
    lowercase_chars = string.lowercase
    digits = string.digits
    special_chars = '!"#$%&\()*+,-./:;<=>?@[]^_{|}~'
    length = 8

    def __init__(self):
        self.char_choices = [self.uppercase_chars,
                             self.lowercase_chars,
                             self.digits,
                             self.special_chars]

    def _make_choice_copy(self):
        return copy.copy(self.char_choices)

    def generate(self, length=None):
        pass_length = length or self.length
        char_copy = self._make_choice_copy()
        final_password = []

        for _ in range(pass_length):
            if not char_copy:
                char_copy = self._make_choice_copy()

            char_choice = char_copy.pop(char_copy.index(random.choice(char_copy)))
            final_password.append(random.choice(char_choice))

        return "".join(final_password)
