from enum import Enum
from fastapi import FastAPI, Request, HTTPException, status, File, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
from driver import *
import uvicorn


# Load configuration from environment variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

templates = Jinja2Templates(directory="templates")


class VideoQuality(str, Enum):
    best = 'best'
    p2160 = '2160'
    p1440 = '1440'
    p1080 = '1080'
    p720 = '720'
    p480 = '480'
    p360 = '360'
    p240 = '240'
    p144 = '144'


class AudioQuality(str, Enum):
    kbps320 = '320'
    kbps256 = '256'
    kbps192 = '192'
    kbps128 = '128'


class DownloadVideoData(BaseModel):
    url: str
    quality: VideoQuality = VideoQuality.best
    output_directory: str = 'downloads'


class DownloadAudioData(BaseModel):
    url: str
    audio_quality: AudioQuality = AudioQuality.kbps192
    output_directory: str = 'downloads'


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/download/{file_path:path}")
async def download(file_path: str):
    file_path = Path(file_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return FileResponse(file_path)


@app.get("/")
async def read_root():
    return "Hello, World!"


@app.post("/download_video")
async def handle_download_video(data: DownloadVideoData):
    url = data.url
    quality = data.quality
 
    output_directory = data.output_directory
    if url:
        file_path, file_name = download_video(url, quality, output_directory)
        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                headers={"Content-Disposition": f'attachment; filename="{file_name}"'}
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is required")


@app.post("/download_audio")
async def handle_download_audio(data: DownloadAudioData):
    url = data.url
    audio_quality = data.audio_quality
    output_directory = data.output_directory
    if url:
        file_path, file_name = download_audio(url, audio_quality, output_directory)
        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                headers={"Content-Disposition": f'attachment; filename="{file_name}"'}
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is required")


@app.get("/get_video_info")
async def handle_get_video_info(url: str):
    if url:
        video_title, thumbnail_url = get_video_info(url)
        response_data = {"title": video_title, "thumbnail_url": thumbnail_url}
        return response_data
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is required")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
