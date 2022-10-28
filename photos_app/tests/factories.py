import factory
from photos_app.models import Photo


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    title = factory.Faker("word")
    album_ID = factory.Faker("random_digit_not_null")
    photo_url = factory.django.ImageField(format="png")
