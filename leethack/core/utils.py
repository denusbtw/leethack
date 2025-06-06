import uuid

from leethack.core.validators import (
    ImageFormatValidator,
    ImageRatioValidator,
    MinResolutionValidator,
    MaxImageSizeValidator,
    FileValidator,
)


def build_image_validators(config: dict) -> list[FileValidator]:
    return [
        ImageFormatValidator(config),
        ImageRatioValidator(config),
        MinResolutionValidator(config),
        MaxImageSizeValidator(config),
    ]


def generate_unique_filename(filename):
    ext = filename.split(".")[-1]
    return f"{uuid.uuid4().hex}.{ext}"
