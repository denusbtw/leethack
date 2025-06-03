from leethack.core.validators import (
    ImageFormatValidator,
    ImageRatioValidator,
    MinResolutionValidator,
    MaxImageSizeValidator,
)


def build_image_validators(config):
    return [
        ImageFormatValidator(config),
        ImageRatioValidator(config),
        MinResolutionValidator(config),
        MaxImageSizeValidator(config),
    ]
