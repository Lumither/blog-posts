import mimetypes

import manifest
from config import POST_PATH, MEDIA_PATH
from image import img_workflow
from log import logger_init
from utils import get_images, post_rpath_str, hash_file


def main():
    log = logger_init("main")

    lock = manifest.load()

    walked_images = {}

    image_paths = get_images(POST_PATH)

    MEDIA_PATH.mkdir(parents=True, exist_ok=True)

    for image in image_paths:
        stat = image.stat()

        identifier = post_rpath_str(image)
        size = stat.st_size
        mime = mimetypes.guess_file_type(image.name)
        img_hash = hash_file(image)

        record = lock.get(identifier)
        if record and record['size'] == size and record['hash'] == img_hash:
            log.info(f"skipping {identifier}")
            walked_images[identifier] = record
            continue

        log.info(f"===== START {identifier} =====")
        try:
            imgs = img_workflow(image, identifier)
            record = {
                "identifier": identifier,
                "hash": img_hash,
                "size": size,
                "mime": mime[0],
                "payload": imgs
            }
            lock[identifier] = record
        except Exception as e:
            log.error(f"failed to process {identifier}: {e}")
        log.info(f"====== END {identifier} ======")

    manifest.save(lock)


if __name__ == "__main__":
    main()
