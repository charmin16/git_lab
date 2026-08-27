import uuid
import os
import filetype
from pathlib import Path
from fastapi import UploadFile, File
from fastapi import HTTPException
import shutil

ALLOWED_PHOTO_FILES = {"image/jpeg", "image/jpg", "image/png"}
ALLOWED_VIDEO_FILES = {"video/mp4", "video/quicktime"}

MAX_ALLOWED_PHOTO = 10 * 1024 * 1024
MAX_ALLOWED_VIDEO = 50 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024

upload_dir = Path(__file__).resolve().parent / "upload_dir"
upload_dir.mkdir(exist_ok=True)

# this is just for practice
upload = Path(__file__).resolve().parent / "upload"
upload.mkdir(exist_ok=True)

photo_dir = upload / "photos"
photo_dir.mkdir(parents=True, exist_ok=True)

video_dir = upload / "videos"
video_dir.mkdir(parents=True, exist_ok=True)


def verify_photo(photo: UploadFile = File()):
    content = photo.file
    content_read = photo.file.read()

    file_type = filetype.guess(content)
    if file_type.mime not in ALLOWED_PHOTO_FILES:
        raise HTTPException(400, "Incorrect Filetype, Photos Only")
    content.seek(0)

    # alternatively
    # if len(content_read) > MAX_ALLOWED_PHOTO:
    #    raise HTTPException(400, "file size too big, maximum is 10mb")

    content.seek(0, 2)
    size = content.tell()
    content.seek(0)

    if size > MAX_ALLOWED_PHOTO:
        raise HTTPException(400, "file size too big, maximum is 10mb")

    extension = Path(photo.filename).suffix
    gen_name = f"{uuid.uuid4()}{extension}"
    filepath = photo_dir / gen_name

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(content, buffer)

    return {
        "filename": photo.filename,
        "filepath": filepath,
        "media_type": photo.content_type,
        "generated_name": gen_name
    }


# verify video
def verify_video(video: UploadFile = File()):
    video_file = video.file

    kind = filetype.guess(video_file)
    if kind.mime not in ALLOWED_VIDEO_FILES:
        raise HTTPException(400, "Video only")

    video_file.seek(0)

    video_file.seek(0, 2)
    size = video_file.tell()

    if size > MAX_ALLOWED_VIDEO:
        raise HTTPException(400, "video size can not exceed 40MB")

    extension = Path(video.filename).suffix
    gen_video_name = f"{uuid.uuid4()}{extension}"
    video_path = video_dir / gen_video_name

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video_file, buffer)

    return {
        "filename": video.filename,
        "filepath": video_path,
        "video_gen": gen_video_name,
        "content_type": video.content_type
    }














