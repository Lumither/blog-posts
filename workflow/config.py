from pathlib import Path

POST_PATH = Path(__file__).parent.parent / 'posts'

DIST_PATH = Path(__file__).parent.parent / 'dist'
LOCK_FILE = DIST_PATH / 'media.lock'
MEDIA_PATH = DIST_PATH / 'media'
