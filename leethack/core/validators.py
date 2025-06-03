from PIL import Image, UnidentifiedImageError
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import math


class BaseImageValidator:
    def open_image(self, file):
        try:
            image = Image.open(file)
            image.verify()
            file.seek(0)
            image = Image.open(file)
            image.load()
            file.seek(0)
            return image
        except (UnidentifiedImageError, OSError):
            raise ValidationError(_("Invalid or corrupted image file."))


class ImageRatioValidator(BaseImageValidator):
    def __init__(self, config):
        self.ratio = config.get("ratio")

    def __call__(self, file):
        return self.validate(file)

    def validate(self, file):
        image = self.open_image(file)
        if not math.isclose(image.width / image.height, self.ratio[0], rel_tol=1e-2):
            raise ValidationError(
                _(f"Image must have {self.ratio[1]} resolution ratio.")
            )


class ImageFormatValidator(BaseImageValidator):
    def __init__(self, config):
        self.allowed_formats = config.get("allowed_formats")

    def __call__(self, file):
        return self.validate(file)

    def validate(self, file):
        image = self.open_image(file)
        if not image.format:
            raise ValidationError(_("Could not determine image format."))

        if image.format.strip().lower() not in self.allowed_formats:
            raise ValidationError(
                _(
                    "Image must have allowed formats: {}".format(
                        ", ".join(sorted(self.allowed_formats))
                    )
                )
            )


class MinResolutionValidator(BaseImageValidator):
    def __init__(self, config):
        self.min_width = config.get("min_width")
        self.min_height = config.get("min_height")

    def __call__(self, file):
        return self.validate(file)

    def validate(self, file):
        image = self.open_image(file)
        if image.width < self.min_width or image.height < self.min_height:
            raise ValidationError(
                _(f"Image must be at least {self.min_width}x{self.min_height}.")
            )


class MaxImageSizeValidator:
    def __init__(self, config):
        self.max_size_mb = config.get("max_size_mb")
        self.max_bytes = int(self.max_size_mb * 1024 * 1024)

    def __call__(self, file):
        return self.validate(file)

    def validate(self, file):
        size = getattr(file, "size", None)
        if size is None:
            raise ValidationError(_("Could not determine file size."))

        if size > self.max_bytes:
            uploaded_file_size = round(size / 1024 / 1024, 2)
            raise ValidationError(
                _(
                    f"Image file size must be under {self.max_size_mb}MB."
                    f" Uploaded file size: {uploaded_file_size}MB."
                )
            )
