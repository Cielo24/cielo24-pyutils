# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import boto3
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class S3TemporaryUrlBaseView(APIView):
    access_key = None
    secret_key = None
    content_type = None
    expiration = 3600
    s3_method = 'PUT'
    bucket = None
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        if not self.access_key or not self.secret_key:
            raise NotImplementedError(
                'You must override access_key and secret_key '
                'to be able to connect to the bucket.'
            )

        if not self.bucket:
            raise NotImplementedError(
                'You must provide a bucket name to this class in order to '
                'generate urls for upload.'
            )

        if not self.content_type:
            raise NotImplementedError(
                'You must provide a content_type for this class otherwise '
                'you won\'t be able to upload files to the bucket.'
            )

        self.client = boto3.client('s3',
                                   aws_access_key_id=self.access_key,
                                   aws_secret_access_key=self.secret_key)

        super(S3TemporaryUrlBaseView, self).__init__(**kwargs)

    def make_key(self, key):
        """
        Method to override to provide a custom way to forge a unique
        key for the upload.
        """
        return key

    def post(self, request):
        client_key = request.data.get('bucket_key')

        if not client_key:
            return Response({'bad_request': 'missing_key'}, status.HTTP_400_BAD_REQUEST)

        key = self.make_key(client_key)
        temp_url = self.client.generate_presigned_url(
            'put_object',
            Params={'Bucket': self.bucket,
                    'Key': key,
                    'ContentType': self.content_type},
            ExpiresIn=self.expiration,
            HttpMethod=self.s3_method
        )

        return Response({'url': temp_url})
