from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess
import sys
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class VideoInput(BaseModel):
    url: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/downloader')
def download_youtube_video(request: VideoInput):
    url = request.url
    try:
        print(f"Starting download for: {url}")
        result = subprocess.run(
            ["yt-dlp", "-f", "mp4", "-o", "%(title)s.%(ext)s", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            print("✅ Download successful!")
            return JSONResponse(content={"message": "Download successful", "output": result.stdout}, status_code=200)
        else:
            print("❌ Download failed!")
            return JSONResponse(content={"error": "Download failed", "details": result.stderr}, status_code=500)

    except FileNotFoundError:
        return JSONResponse(content={"error": "yt-dlp is not installed or not in PATH"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"Unexpected error: {e}"}, status_code=500)


if __name__=="__main__":
    uvicorn.run(app,reload=True,port=8000)
