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
