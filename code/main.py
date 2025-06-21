from fastapi import FastAPI, HTTPException
from video_downloader import VideoInput
from video_downloader import download_video, get_video_info, is_valid_youtube_url, downloaded_videos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/download/resolution')
def downloader(video_input: VideoInput):
    url = video_input.url
    resolution = video_input.resolution

    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter in the request body.")

    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")
    
    success, error_message = download_video(video_input)

    if success:
        return {"message": f"Video with resolution {resolution} downloaded successfully."}
    else:
        raise HTTPException(status_code=400, detail=error_message)

@app.post('/video_info')
def video_info(video_input: VideoInput):
    if not video_input.url:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter in the request body.")

    if not is_valid_youtube_url(video_input.url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")
    
    video_data, error = get_video_info(video_input)

    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return video_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
