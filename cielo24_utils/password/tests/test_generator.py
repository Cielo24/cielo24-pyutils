# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from ..generator import RandomPasswordGenerator
from ..validators import PasswordValidator


class RandomPasswordGeneratorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(RandomPasswordGeneratorTestCase, cls).setUpClass()
        cls.validator = PasswordValidator
        cls.generator = RandomPasswordGenerator()

    def test_password_length_ok(self):
        password = self.generator.generate(10)

        self.assertEqual(len(password), 10)

    def test_password_meets_requirements(self):
        password = self.generator.generate(12)
        validator = self.validator(password)

        self.assertTrue(validator.is_valid())

    def test_password_does_not_meet_requirements(self):
        password1 = self.generator.generate(129)
        password2 = self.generator.generate(7)
        validator1 = self.validator(password1)
        validator2 = self.validator(password2)

        self.assertFalse(validator1.is_valid())
        self.assertFalse(validator2.is_valid())
