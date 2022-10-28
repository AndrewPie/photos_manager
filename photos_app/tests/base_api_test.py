import pytest
from django.db import models
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class BaseApiTest:
    CLIENT = APIClient()
    APP_BASENAME = ""

    def _test_read_objects_list(
        self, serializer: serializers.ListSerializer, object_count: int
    ):
        response = self.CLIENT.get(reverse(f"{self.APP_BASENAME}-list"))
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.data.get("count") == object_count
        assert response.data.get("results") == serializer.data

    def _test_read_object_detail(
        self, serializer: serializers.ModelSerializer, requested_object: models.Model
    ):
        response = self.CLIENT.get(
            reverse(f"{self.APP_BASENAME}-detail", args=[requested_object.id])
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        for key in response.data.keys():
            assert response.data[key] == serializer.data.get(key)
