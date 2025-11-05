import logging
from io import BytesIO
from math import floor
from pathlib import Path

from PIL import Image, ImageFilter
from PIL.Image import Resampling
from PIL.ImageFile import ImageFile

from config import MEDIA_PATH
from log import with_logger
from utils import encode_media_fname

EXPECTED_FORMAT = ['webp', 'png']


@with_logger("image.cvt_colormodel")
def cvt_colormodel(img: ImageFile,
                   log: logging.Logger | None = None) -> ImageFile:
    if img.mode != 'RGB' and img.mode != 'RGBA':
        img = img.convert('RGB')
        log.debug("converted to RGB color model")
    return img


@with_logger("image.downscale")
def downscale_img(img: ImageFile,
                  scale: float = 1,
                  log: logging.Logger | None = None) -> ImageFile:
    assert 0 <= scale <= 1.0

    o_width, o_height = img.size
    n_width, n_height = floor(o_width * scale), floor(o_height * scale)

    log.debug(f"downscaling image from {o_width}x{o_height} to {n_width}x{n_height}")
    rsz_img = img.resize((n_width, n_height), Resampling.LANCZOS)
    log.debug("success")

    return rsz_img


@with_logger("image.cvt")
def convert_img(img: ImageFile,
                quality: int = 100,
                output_format: str = 'webp',
                log: logging.Logger | None = None) -> ImageFile:
    assert output_format in EXPECTED_FORMAT
    assert 0 <= quality <= 100

    log.debug(f"converting image to {output_format} with quality {quality}")

    buf = BytesIO()
    img.save(buf, output_format, quality=quality)
    buf.seek(0)

    log.debug("success")

    return Image.open(buf)


@with_logger("image.blur")
def blur_img(image: ImageFile,
             radius: int = 10,
             log: logging.Logger | None = None) -> ImageFile:
    assert 0 <= radius <= 100

    log.debug(f"blurring image with radius {radius}")
    img = image.filter(ImageFilter.GaussianBlur(radius=radius))
    log.debug("success")

    return img


@with_logger("image.write")
def write_img(image: ImageFile,
              path: Path,
              log: logging.Logger | None = None) -> None:
    try:
        log.debug(f"writing image to {path}")
        image.save(path)
        log.debug("success")
    except Exception as e:
        log.error(f"failed to write: {path}: {e}")
        raise


@with_logger("image.workflow")
def img_workflow(image: Path,
                 identifier: str,
                 log: logging.Logger | None = None) -> list[str]:
    log.info(f"processing {identifier}")

    variants = {
        "x": 0.8,
        "m": 0.5,
        "s": 0.25,
    }
    img_ext = "webp"

    with Image.open(image) as img:
        img_c = cvt_colormodel(img)

        imgs: list[str] = []

        def build_path(id_str: str, p_fix: str | None = None, ext: str | None = None, id_only=False) -> Path:
            path = MEDIA_PATH / id_str
            path.parent.mkdir(parents=True, exist_ok=True)
            if id_only:
                return path
            return MEDIA_PATH / encode_media_fname(id_str, p_fix, ext)

        for postfix, scale in variants.items():
            img_v = downscale_img(img_c, scale)
            img_v_path = build_path(identifier, postfix, img_ext)
            imgs.append(img_v_path.relative_to(MEDIA_PATH).as_posix())

            log.info(f"writing {postfix} variant as {img_v_path}")
            write_img(img_v, img_v_path)

        img_blr = blur_img(downscale_img(img_c, 0.5))
        img_blr_path = build_path(identifier, "b", img_ext)
        imgs.append(img_blr_path.relative_to(MEDIA_PATH).as_posix())
        log.info(f"writing b variant as {img_blr_path}")
        write_img(img_blr, img_blr_path)

        img_o_path = build_path(identifier, id_only=True)
        imgs.append(img_o_path.relative_to(MEDIA_PATH).as_posix())
        log.info(f"writing original as {img_o_path}")
        write_img(img, img_o_path)

    return imgs
