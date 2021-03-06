# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from ..views import S3TemporaryUrlBaseView


class S3MissingCredentialsView(S3TemporaryUrlBaseView):
    bucket = 'py-test-dev'
    content_type = 'text/csv'


class S3TempUrlView(S3TemporaryUrlBaseView):
    access_key = 'AcCeSsKey'
    secret_key = 'SeCrEtKeY'
    bucket = 'py-test-dev'
    content_type = 'text/csv'


class S3MissingBucketView(S3TemporaryUrlBaseView):
    access_key = 'AcCeSsKey'
    secret_key = 'SeCrEtKeY'
    content_type = 'text/csv'


class S3MissingContentTypeView(S3TemporaryUrlBaseView):
    access_key = 'AcCeSsKey'
    secret_key = 'SeCrEtKeY'
    bucket = 'py-test-dev'


class S3CustomKeyTempUrlView(S3TempUrlView):

    def make_key(self, key, file_name):
        return key + 'custom' + file_name


class S3TempUrlBaseTest(APITestCase):
    username = 'TestUser'
    password = 'PassyPassword'

    def setUp(self):
        super(S3TempUrlBaseTest, self).setUp()
        self.factory = APIRequestFactory()
        self.view = S3TempUrlView.as_view()

    def test_post_403(self):
        request = self.factory.post('/', format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_bucket(self):
        request = self.factory.post('/', format='json')

        with self.assertRaises(NotImplementedError):
            S3MissingBucketView.as_view()(request)

    def test_missing_credentials(self):
        request = self.factory.post('/', format='json')

        with self.assertRaises(NotImplementedError):
            S3MissingCredentialsView.as_view()(request)

    def test_missing_content_type(self):
        request = self.factory.post('/', format='json')

        with self.assertRaises(NotImplementedError):
            S3MissingContentTypeView.as_view()(request)

    @pytest.mark.django_db
    def test_missing_key_post(self):
        user = User.objects.create_user(self.username, self.password)
        request = self.factory.post('/', format='json')
        force_authenticate(request, user=user)

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_missing_file_name_post(self):
        user = User.objects.create_user(self.username, self.password)
        request = self.factory.post('/', {'bucket_key': 'test-key'}, format='json')
        force_authenticate(request, user=user)

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_post_ok(self):
        key = 'test-key'
        user = User.objects.create_user(self.username, self.password)
        request = self.factory.post('/',
                                    {'bucket_key': key, 'file_name': 'asd.csv'},
                                    format='json')
        force_authenticate(request, user=user)

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(key, response.content)

    @pytest.mark.django_db
    def test_post_ok_custom_key(self):
        key = 'test-key'
        file_name = 'asd.csv'
        view = S3CustomKeyTempUrlView.as_view()
        user = User.objects.create_user(self.username, self.password)
        request = self.factory.post('/',
                                    {'bucket_key': key, 'file_name': 'asd.csv'},
                                    format='json')
        force_authenticate(request, user=user)

        response = view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(key + 'custom' + file_name, response.content)
