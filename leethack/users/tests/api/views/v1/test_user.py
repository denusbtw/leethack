import pytest
from django.urls import reverse


@pytest.fixture
def me_detail_url():
    return reverse("api:v1:me_detail")


@pytest.mark.django_db
class TestMeDetailAPIView:
    pass
