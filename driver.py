import yt_dlp
from yt_dlp.postprocessor.common import PostProcessor

class FilePathLogger(PostProcessor):
    def run(self, information):
        self.file_path = information['filepath']
        return [], information
    
def download_video(url, quality='best', output_directory='downloads'):
    format_option = {
        '2160': 'bestvideo[height=2160]+bestaudio/best[height=2160]',
        '1440': 'bestvideo[height=1440]+bestaudio/best[height=1440]',
        '1080': 'bestvideo[height=1080]+bestaudio/best[height=1080]',
        '720': 'bestvideo[height=720]+bestaudio/best[height=720]',
        '480': 'bestvideo[height=480]+bestaudio/best[height=480]',
        '360': 'bestvideo[height=360]+bestaudio/best[height=360]',
        'best': 'bestvideo+bestaudio/best'
    }.get(quality, 'bestvideo+bestaudio/best')  # default to best quality if an invalid quality is provided
    
    ydl_opts = {
        'format': format_option,
        'outtmpl': f'{output_directory}/%(title)s.%(ext)s',
        'ffmpeg_location': 'ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin',  # ensure you have ffmpeg downloaded
        'postprocessors': [FilePathLogger()]
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return ydl.postprocessors[0].file_path  # Return the file path

def download_audio(url, audio_quality='192', output_directory='downloads'):
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
        info_dict = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info_dict)
        ydl.download([url])
        return filename  # Return the filename


        
# low: 128, medium: 192, high: 256, exepctional: 320
#download_audio(video_url)  # To download the audio
#TODO logging

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
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


