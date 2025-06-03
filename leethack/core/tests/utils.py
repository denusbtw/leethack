import io

import numpy as np
from PIL import Image


def create_test_image(
    size=(200, 200),
    fmt="JPEG",
    mode="RGB",
    target_size_kb=None,
    quality_step=5,
    max_attempts=20,
):
    if target_size_kb is None:
        byte_array = io.BytesIO()
        image = Image.new(mode, size)
        image.save(byte_array, fmt)
        byte_array.seek(0)
        return byte_array

    target_bytes = target_size_kb * 1024
    fmt_upper = fmt.upper()

    def save_image(image, **save_kwargs):
        byte_array = io.BytesIO()
        image.save(byte_array, format=fmt_upper, **save_kwargs)
        byte_array.seek(0)
        return byte_array

    if fmt_upper == "JPEG":
        image = Image.new(mode, size)
        for quality in range(100, 0, -quality_step):
            byte_array = save_image(image, quality=quality)
            if byte_array.getbuffer().nbytes >= target_bytes:
                return byte_array
    else:
        current_size = size
        for _ in range(max_attempts):
            array = np.random.randint(
                0, 256, (current_size[1], current_size[0], len(mode)), dtype=np.uint8
            )
            image = Image.fromarray(array, mode)
            byte_array = save_image(image)
            if byte_array.getbuffer().nbytes >= target_bytes:
                return byte_array
            current_size = (int(current_size[0] * 1.5), int(current_size[1] * 1.5))

    raise ValueError("Cannot reach target size with current parameters.")
