from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from driver import *

app = FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root():
    return "Hello, World!"


class DownloadVideoData(BaseModel):
    url: str
    quality: str = 'best'
    output_directory: str = 'downloads'


@app.post("/download_video")
async def handle_download_video(data: DownloadVideoData):
    url = data.url
    quality = data.quality
    output_directory = data.output_directory
    if url:
        download_video(url, quality, output_directory)
        return {"message": "Video downloaded successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is required")


class DownloadAudioData(BaseModel):
    url: str
    audio_quality: str = '192'
    output_directory: str = 'downloads'


@app.post("/download_audio")
async def handle_download_audio(data: DownloadAudioData):
    url = data.url
    audio_quality = data.audio_quality
    output_directory = data.output_directory
    if url:
        download_audio(url, audio_quality, output_directory)
        return {"message": "Audio downloaded successfully"}
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
