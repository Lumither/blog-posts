import hashlib
from pathlib import Path
from urllib.parse import quote

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
    year_striped = Path(*relative_path.parts[1:])
    return year_striped.as_posix()


def encode_media_fname(identifier: str, postfix: str | None, ext: str | None) -> str:
    filename = identifier
    if postfix is not None:
        filename += f"+{postfix}"
    if ext is not None:
        filename += f".{ext}"
    return quote(filename, safe="")
