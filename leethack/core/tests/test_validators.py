import pytest
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from .utils import create_test_image
from ..validators import (
    ImageRatioValidator,
    ImageFormatValidator,
    MinResolutionValidator,
    MaxImageSizeValidator,
)


class TestImageRatioValidator:

    def test_invalid_image(self):
        invalid_file = SimpleUploadedFile(
            "invalid.jpg", b"not an image content", content_type="image/jpeg"
        )

        validator = ImageRatioValidator({"ratio": (1, "1:1")})
        with pytest.raises(ValidationError) as exc_info:
            validator(invalid_file)
        assert "Invalid or corrupted image file." in str(exc_info.value)

    def test_error(self):
        image_file = create_test_image(size=(100, 100))
        uploaded_file = SimpleUploadedFile(
            "test.jpg", image_file.read(), content_type="image/jpeg"
        )
        image_file.seek(0)

        validator = ImageRatioValidator({"ratio": (2 / 1, "2:1")})
        with pytest.raises(ValidationError) as exc_info:
            validator(uploaded_file)
        assert "2:1" in str(exc_info.value)

    def test_no_error(self):
        image_file = create_test_image(size=(200, 100))
        uploaded_file = SimpleUploadedFile(
            "test.jpg", image_file.read(), content_type="image/jpeg"
        )
        image_file.seek(0)

        validator = ImageRatioValidator({"ratio": (2 / 1, "2:1")})
        validator(uploaded_file)


class TestImageFormatValidator:

    def test_invalid_image(self):
        invalid_file = SimpleUploadedFile(
            "invalid.jpg", b"not an image content", content_type="image/jpeg"
        )

        validator = ImageRatioValidator({"ratio": (1, "1:1")})
        with pytest.raises(ValidationError) as exc_info:
            validator(invalid_file)
        assert "Invalid or corrupted image file." in str(exc_info.value)

    def test_error(self):
        image_file = create_test_image(fmt="PNG")
        uploaded_file = SimpleUploadedFile(
            "test.png", image_file.read(), content_type="image/png"
        )
        image_file.seek(0)

        validator = ImageFormatValidator({"allowed_formats": {"jpeg", "webp"}})
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(uploaded_file)
        assert "Image must have allowed formats" in str(exc_info.value)

    def test_no_error(self):
        image_file = create_test_image(fmt="PNG")
        uploaded_file = SimpleUploadedFile(
            "test.png", image_file.read(), content_type="image/png"
        )
        image_file.seek(0)

        validator = ImageFormatValidator({"allowed_formats": {"png", "webp"}})
        validator.validate(uploaded_file)


class TestMinResolutionValidator:

    def test_invalid_image(self):
        invalid_file = SimpleUploadedFile(
            "invalid.jpg", b"not an image content", content_type="image/jpeg"
        )

        validator = ImageRatioValidator({"ratio": (1, "1:1")})
        with pytest.raises(ValidationError) as exc_info:
            validator(invalid_file)
        assert "Invalid or corrupted image file." in str(exc_info.value)

    def test_error(self):
        image_file = create_test_image(size=(100, 100))
        uploaded_file = SimpleUploadedFile(
            "test.jpg", image_file.read(), content_type="image/jpeg"
        )

        validator = MinResolutionValidator({"min_width": 120, "min_height": 120})
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(uploaded_file)
        assert "120x120" in str(exc_info.value)

    def test_no_error(self):
        image_file = create_test_image(size=(120, 120))
        uploaded_file = SimpleUploadedFile(
            "test.jpg", image_file.read(), content_type="image/jpeg"
        )

        validator = MinResolutionValidator({"min_width": 120, "min_height": 120})
        validator.validate(uploaded_file)


class TestMaxImageSizeValidator:

    def test_invalid_image(self):
        invalid_file = SimpleUploadedFile(
            "invalid.jpg", b"not an image content", content_type="image/jpeg"
        )

        validator = ImageRatioValidator({"ratio": (1, "1:1")})
        with pytest.raises(ValidationError) as exc_info:
            validator(invalid_file)
        assert "Invalid or corrupted image file." in str(exc_info.value)

    def test_error(self):
        image_file = create_test_image(target_size_kb=2000, size=(500, 500), fmt="PNG")
        uploaded_file = SimpleUploadedFile(
            "test.png", image_file.read(), content_type="image/png"
        )

        validator = MaxImageSizeValidator({"max_size_mb": 1})
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(uploaded_file)
        assert "must be under 1MB." in str(exc_info.value)

    def test_no_error(self):
        image_file = create_test_image(target_size_kb=500, size=(500, 500), fmt="PNG")
        uploaded_file = SimpleUploadedFile(
            "test.png", image_file.read(), content_type="image/png"
        )

        validator = MaxImageSizeValidator({"max_size_mb": 1})
        validator.validate(uploaded_file)
