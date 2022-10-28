from io import BytesIO

import pytest
import requests
import responses
from photos_app.models import Photo
from photos_app.serializers import PhotoSerializer
from photos_app.tests.base_api_test import BaseApiTest
from PIL import Image
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def mocked_response():
    bytes_stream = BytesIO()
    sample_image = Image.open("sample_image.png")
    sample_image.save(bytes_stream, format="PNG")
    bytes_stream.seek(0)
    responses.add(
        responses.GET,
        "http://example.org/photos/my_image.png",
        body=bytes_stream.getvalue(),
        status=200,
        content_type="image/png",
    )


class TestPhotosApi(BaseApiTest):
    APP_BASENAME = "photo"

    @pytest.fixture(autouse=True)
    def fixture_photos(self, photo_factory):
        self.photo1 = photo_factory()
        self.photo2 = photo_factory()

    def test_read_photos_list(self):
        db_photos = Photo.objects.all()
        serializer = PhotoSerializer(
            db_photos,
            many=True,
            context={"request": Request(factory.get("/"))},
        )
        self._test_read_objects_list(serializer=serializer, object_count=2)

    def test_read_photo_detail(self):
        db_photo = Photo.objects.get(pk=self.photo1.id)
        serializer = PhotoSerializer(
            db_photo,
            context={"request": Request(factory.get("/"))},
        )
        self._test_read_object_detail(
            serializer=serializer, requested_object=self.photo1
        )

    @responses.activate
    def test_external_api_mocking(self):
        response = requests.get("http://example.org/photos/my_image.png")
        assert response.status_code == status.HTTP_200_OK, response.text
        assert type(response.content) == bytes
