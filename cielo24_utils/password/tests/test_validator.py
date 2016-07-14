# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from ..validators import PasswordValidator


class PasswordValidatorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(PasswordValidatorTestCase, cls).setUpClass()
        cls.validator = PasswordValidator

    def test_password_too_short(self):
        password = self.validator('Sh0rt@')

        self.assertFalse(password.is_valid())
        self.assertIn('minimum', ", ".join(password.errors))

    def test_password_too_long(self):
        password = self.validator('V3ryl0ngpassword' + ('d' * 150))

        self.assertFalse(password.is_valid())
        self.assertIn('maximum', ", ".join(password.errors))

    def test_no_digits_in_password(self):
        password = self.validator('Nodigit@pass')

        self.assertFalse(password.is_valid())
        self.assertIn('digit', ", ".join(password.errors))

    def test_no_uppercase_in_password(self):
        password = self.validator('n0upperc@ase')

        self.assertFalse(password.is_valid())
        self.assertIn('uppercase', ", ".join(password.errors))

    def test_no_lowercase_in_password(self):
        password = self.validator('N0LOWERC@ASE')

        self.assertFalse(password.is_valid())
        self.assertIn('lowercase', ", ".join(password.errors))

    def test_no_special_char_in_password(self):
        password = self.validator('Nospecia1char')

        self.assertFalse(password.is_valid())
        self.assertIn('special', ", ".join(password.errors))

    def test_good_password(self):
        password = self.validator('Verys3cretP@ss')

        self.assertTrue(password.is_valid())
        self.assertEqual(password.errors, [])
