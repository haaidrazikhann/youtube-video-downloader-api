from pydantic import BaseModel
from pytube import YouTube
import re

class VideoInput(BaseModel):
    url: str
    resolution:str = None

downloaded_videos = []

def download_video(video_input: VideoInput):
    try:
        yt = YouTube(video_input.url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=video_input.resolution).first()
        if stream:
            video = stream.download()
            downloaded_videos.append(video)
        else:
            return False, "Video with the specified resolution not found."
    except Exception as e:
        return False, str(e)
    
def get_video_info(video_input: VideoInput):
    try:
        yt = YouTube(video_input.url)
        stream = yt.streams.first()
        video_info = {
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "views": yt.views,
            "description": yt.description,
            "publish_date": yt.publish_date,
        }
        return video_info, None
    except Exception as e:
        return None, str(e)

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$"
    return re.match(pattern, url) is not None

