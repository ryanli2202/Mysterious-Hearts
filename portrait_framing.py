"""Aspect-preserving stature fitting for cropped character illustrations.

The lower thighs, knees and feet are outside these portraits. Their visible
head-to-mid-thigh span represents about 70% of stature, not a full standing
body. The bottom is a shared picture crop, not a floor/foot position. This
doesn't synthesize legs or stretch bodies. Older bust/waist compositions still
need their planned artwork replacements for consistent anatomical coverage.
"""
from functools import lru_cache
from pathlib import Path

from PIL import Image

VISIBLE_BODY_FRACTION = .70
REFERENCE_HEIGHT_CM = 211  # Tallest authored master; do not flatten taller people at the cap.


def visible_bounds(image):
    # Almost-transparent export padding must not decide a character's height.
    return image.getchannel('A').point(lambda a: 255 if a >= 16 else 0).getbbox()


@lru_cache(maxsize=48)
def _load(path, modified):
    with Image.open(path) as source:
        image = source.convert('RGBA')
    box = visible_bounds(image)
    return image.crop(box) if box else image


def load(path):
    path = Path(path)
    return _load(str(path), path.stat().st_mtime_ns)


def capacity(image, size, height_cm):
    """Largest shared pixels/cm that fits this whole cropped illustration."""
    visible_cm = height_cm * VISIBLE_BODY_FRACTION
    return min(size[1] / visible_cm,
               size[0] * image.height / (image.width * visible_cm))


def shared_scale(portraits):
    """Use the tightest participant slot for EVERY person, including player."""
    return min(capacity(image, size, height) for image, size, height in portraits)


def fit(image, size, height_cm, scale=None):
    if scale is None:
        reference_pixels = min(size[1], size[0] * 1.5)
        scale = min(reference_pixels / (REFERENCE_HEIGHT_CM * VISIBLE_BODY_FRACTION),
                    capacity(image, size, height_cm))
    target_height = max(1, round(height_cm * VISIBLE_BODY_FRACTION * scale))
    target_width = max(1, round(image.width * target_height / image.height))
    # At most one pixel of rounding adjustment, never independently compress x/y.
    factor = min(1, size[0] / target_width, size[1] / target_height)
    dimensions = (max(1, round(target_width * factor)), max(1, round(target_height * factor)))
    art = image.resize(dimensions, Image.Resampling.LANCZOS)
    frame = Image.new('RGBA', size, (0, 0, 0, 0))
    frame.alpha_composite(art, ((size[0] - art.width) // 2, size[1] - art.height))
    return frame
