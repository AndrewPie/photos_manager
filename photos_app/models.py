import uuid

from django.db import models


def get_upload_path(instance, filename):
    return f"photos/album_{instance.album_ID}/{str(uuid.uuid4())}{filename}"


class Photo(models.Model):
    title = models.CharField(max_length=255, unique=True)
    album_ID = models.IntegerField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    dominant_color = models.CharField(max_length=7, null=True, blank=True)
    photo_url = models.ImageField(
        upload_to=get_upload_path,
        width_field="width",
        height_field="height",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["album_ID", "title"]

    def __str__(self):
        return f"{self.album_ID} - {self.title}"
