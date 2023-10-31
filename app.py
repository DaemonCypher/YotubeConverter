from fastapi import FastAPI, Request, HTTPException, status, File, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
from driver import *
import os
import uvicorn

app = FastAPI()

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

templates = Jinja2Templates(directory="templates")


class DownloadVideoData(BaseModel):
    url: str
    quality: str = Query(default='best', regex='^(best|2160|1440|1080|720|480|360|240|144)$')
    output_directory: str = 'downloads'


class DownloadAudioData(BaseModel):
    url: str
    audio_quality: str = Query(default='192', regex='^(320|256|192|128)$')
    output_directory: str = 'downloads'


@app.get("/download/{file_path:path}")
async def download(file_path: str):
    file_path = Path(file_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return FileResponse(file_path)


@app.get("/")
async def read_root():
    return "Hello, World!"


def write_file(file_path: str, content: bytes):
    with open(file_path, "wb") as f:
        f.write(content)


@app.post("/download_video")
async def handle_download_video(data: DownloadVideoData):
    url = data.url
    quality = data.quality
    output_directory = data.output_directory
    if url:
        file_path, file_name = download_video(url, quality, output_directory)
        print(quality)  # Print the quality for debugging
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
