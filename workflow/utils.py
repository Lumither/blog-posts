import hashlib
from pathlib import Path

import base58

from config import POST_PATH


def get_images(path: Path, exts: set[str] = None) -> list[Path]:
    if exts is None:
        exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

    paths = []

    for file in path.rglob('*'):
        if file.suffix.lower() in exts:
            paths.append(file)

    return paths


def hash_file(path: Path, block_size: int = 65536) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)

    return h.hexdigest()


def post_rpath_str(abs_path: Path) -> str:
    assert abs_path.is_absolute()
    relative_path = abs_path.relative_to(POST_PATH)
    cleaned_path = Path(relative_path.parts[1]) / Path(relative_path.parts[-1])
    return cleaned_path.as_posix()


def encode_media_fname(identifier: str, postfix: str | None, ext: str | None) -> str:
    filename = base58.b58encode(identifier.encode("utf-8")).decode("ascii")
    if postfix is not None:
        filename += f"_{postfix}"
    if ext is not None:
        filename += f".{ext}"
    return filename
