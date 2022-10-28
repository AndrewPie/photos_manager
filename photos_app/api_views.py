import json

from django.http import JsonResponse, QueryDict
from rest_framework import serializers, views, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request

from photos_app.models import Photo
from photos_app.serializers import (
    PhotoCreateUpdateSerializer,
    PhotoJSONFileSerializer,
    PhotoSerializer,
)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ("POST", "PUT", "PATCH"):
            serializer_class = PhotoCreateUpdateSerializer
        return serializer_class


class JSONUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def __prepare_data(self, request: Request) -> QueryDict:
        request_data = request.data.copy()
        json_file = request.FILES.get("json_file")
        if not json_file:
            raise serializers.ValidationError(
                {"json_file": ["Proper json_file is necessary"]}
            )
        external_url = json.load(json_file).get("url")
        request_data["external_url"] = external_url
        return request_data

    def post(self, request, format=None):
        a = request
        request_data = self.__prepare_data(request)
        serializer = PhotoJSONFileSerializer(
            data=request_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)
