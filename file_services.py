import uuid
import os
import filetype
from pathlib import Path

ALLOWED_PHOTO_FILES = {"image/jpeg", "image/jpg", "image/png"}
ALLOWED_VIDEO_FILES = {"video/mp4", "video/quicktime"}

MAX_ALLOWED_PHOTO = 10 * 1024 * 1024
MAX_ALLOWED_VIDEO = 50 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024

upload_dir = Path(__file__).resolve().parent / "upload_dir"
upload_dir.mkdir(exist_ok=True)





