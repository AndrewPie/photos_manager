from django.core import files
from django.core.files.base import ContentFile
from rest_framework import serializers

from photos_app.models import Photo
from photos_app.utils import get_photo_data


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "url",
            "id",
            "title",
            "album_ID",
            "width",
            "height",
            "dominant_color",
            "photo_url",
        )


class PhotoCreateUpdateSerializer(serializers.ModelSerializer):
    external_url = serializers.URLField(write_only=True)

    class Meta:
        model = Photo
        fields = (
            "url",
            "id",
            "title",
            "album_ID",
            "width",
            "height",
            "dominant_color",
            "photo_url",
            "external_url",
        )
        read_only_fields = (
            "url",
            "id",
            "width",
            "height",
            "dominant_color",
            "photo_url",
        )

    def create(self, validated_data):
        dominant_color, photo_response = get_photo_data(input_data=validated_data)

        photo = Photo.objects.create(
            title=validated_data.get("title"),
            album_ID=validated_data.get("album_ID"),
            dominant_color=dominant_color,
            photo_url=files.File(ContentFile(photo_response.content), ".png"),
        )
        return photo

    def update(self, instance, validated_data):
        if photo_data := get_photo_data(input_data=validated_data):
            dominant_color, photo_response = photo_data
            instance.dominant_color = dominant_color
            instance.photo_url = files.File(ContentFile(photo_response.content), ".png")

        instance.title = validated_data.get("title", instance.title)
        instance.album_ID = validated_data.get("album_ID", instance.album_ID)
        instance.save()
        return instance


class PhotoJSONFileSerializer(PhotoCreateUpdateSerializer):
    is_from_file = serializers.BooleanField(default=True)

    class Meta(PhotoCreateUpdateSerializer.Meta):
        fields = PhotoCreateUpdateSerializer.Meta.fields + ("is_from_file",)
