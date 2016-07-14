# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class PasswordValidator(object):
    """
    Validates the password basing on the given validation methods.
    To start the validation `.is_valid` should be call, it return either
    True or False, if it returns False `.errors` property can be accessed
    to inspect the errors occured.
    """
    min_length = 8
    max_length = 128
    must_have_min_length = True
    must_have_max_length = True
    must_contain_uppercase = True
    must_contain_lowercase = True
    must_contain_number = True
    must_contain_special_char = True
    special_charset = '!"#$%&\()*+,-./:;<=>?@[]^_{|}~'
    does_not_contain_error = 'Password does not contain any {}'
    does_not_meet_length_error = 'Password does not meet {} length requirements. {} length is {}.'
    first_methods = ['validate_min_length', 'validate_max_length']

    def __init__(self, password):
        self.password = password
        self._errors = []
        self._validation_methods = self._get_validation_methods()

    def _get_validation_methods(self):
        methods = []

        # Be sure the length is checked first, to avoid DOS attacks
        # with long passwords.
        for method in self.first_methods:
            if hasattr(self, method):
                methods.append(method)

        for method in dir(self):
            if method not in self.first_methods and method.startswith('validate'):
                methods.append(method)

        return methods

    def _run_validation(self):
        for method in self._validation_methods:
            error = getattr(self, method)()

            if error:
                self._errors.append(error)

    def is_valid(self):
        self._run_validation()
        self.errors = self._errors
        return not any(self._errors)

    def validate_min_length(self):
        if self.must_have_min_length and not len(self.password) >= self.min_length:
            return self.does_not_meet_length_error.format('minimum', 'Minimum', self.min_length)

    def validate_max_length(self):
        if self.must_have_max_length and not len(self.password) <= self.max_length:
            return self.does_not_meet_length_error.format('maximum', 'Maximum', self.max_length)

    def validate_uppercase(self):
        if self.must_contain_uppercase and not any(char.isupper() for char in self.password):
            return self.does_not_contain_error.format('uppercase character')

    def validate_lowercase(self):
        if self.must_contain_lowercase and not any(char.islower() for char in self.password):
            return self.does_not_contain_error.format('lowercase character')

    def validate_special_char(self):
        if self.must_contain_special_char:
            special_list = []

            for special_char in self.special_charset:
                special_list.append(special_char in self.password)

            if not any(special_list):
                return self.does_not_contain_error.format('special character')

    def validate_number(self):
        if self.must_contain_number and not any(char.isdigit() for char in self.password):
            return self.does_not_contain_error.format('digit')
