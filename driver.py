import yt_dlp
from yt_dlp.postprocessor.common import PostProcessor
import logging

# Constants
OUTPUT_DIRECTORY = 'downloads'
FFMPEG_LOCATION = 'ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin'

# Configure logging
def setup_logging():
    logging.basicConfig(level=logging.INFO)

    
def download_video(url, quality='best', output_directory=OUTPUT_DIRECTORY):
    format_option = {
        '2160': 'bestvideo[height=2160][ext=mp4]+bestaudio[ext=m4a]/best[height=2160]',
        '1440': 'bestvideo[height=1440][ext=mp4]+bestaudio[ext=m4a]/best[height=1440]',
        '1080': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080]',
        '720': 'bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/best[height=720]',
        '480': 'bestvideo[height=480][ext=mp4]+bestaudio[ext=m4a]/best[height=480]',
        '360': 'bestvideo[height=360][ext=mp4]+bestaudio[ext=m4a]/best[height=360]',
        '240': 'bestvideo[height=240][ext=mp4]+bestaudio[ext=m4a]/best[height=240]',
        '144': 'bestvideo[height=144][ext=mp4]+bestaudio[ext=m4a]/best[height=144]',
        'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
    }.get(quality, 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best')  # default to best quality if an invalid quality is provided

    ydl_opts = {
        'format': format_option,
        'outtmpl': f'{output_directory}/%(playlist)s/%(title)s.%(ext)s',  # adjusted to handle playlists
        'ffmpeg_location': 'ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)  # Extract info without downloading
        file_path = ydl.prepare_filename(info_dict)  # Get the file path
        ydl.download([url])  # Now download the video
        video_title = info_dict.get('title', 'video')  # Get the video title or default to 'video' if title is not available
        file_name = f'{video_title}.mp4'  # Construct file name from video title
        return file_path, file_name
    
def download_audio(url, audio_quality='192', output_directory=OUTPUT_DIRECTORY):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_directory}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audio_quality,
        }],
        'ffmpeg_location': 'ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)  # Extract info without downloading
        ydl.download([url])  # Now download the audio
        audio_title = info_dict.get('title', 'audio')  # Get the audio title or default to 'audio' if title is not available
        file_name = f'{audio_title}.mp3'  # Construct file name from audio title
        file_path = f'{output_directory}/{file_name}'  # Update file_path to reflect the .mp3 extension
        return file_path, file_name


def download_playlist_audio(playlist_url, output_directory=OUTPUT_DIRECTORY):
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_directory}/%(playlist)s/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,  # This option suppresses output, remove if you want to see download progress
    }
    
    # Use yt-dlp to extract information about the playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        entries = info_dict.get('entries', [])
        
        for entry in entries:
            video_url = entry['url']
            print(f'Downloading {entry["title"]}...')
            ydl.download([video_url])
            print(f'Downloaded {entry["title"]}.')
        

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,  # Set to False to get detailed info
        'force_generic_extractor': False,  # Set to False to allow specific extractors
        'noplaylist': True,  # Ensure only single video info is retrieved, not playlist info
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

    video_title = video.get('title', None)
    thumbnail_url = video.get('thumbnail', None)

    return video_title, thumbnail_url

if __name__ == "__main__":
    setup_logging()

