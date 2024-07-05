import yt_dlp  # Importing the yt_dlp library for handling YouTube video downloads and information extraction
import logging  # Importing the logging module for logging information, warnings, and errors
import os  # Importing the os module for interacting with the operating system
import shutil  # Importing the shutil module for high-level file operations

# Constants
OUTPUT_DIRECTORY = 'downloads'  # Defining a constant for the directory where downloads will be saved
FFMPEG_LOCATION = 'ffmpeg-master-latest-win64-gpl\\bin'  # Defining a constant for the location of ffmpeg binary

# Configuration for ydl_opt is from https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L183

def setup_logging():
    """Configures logging settings."""
    logging.basicConfig(level=logging.INFO)  # Setting the logging level to INFO


def clear_downloads_folder(output_directory):
    """
    Clears the contents of the downloads folder and help keep the code 
    space managable.
    
    Parameters:
    - output_directory (str): The path to the directory to be cleared.
    """
    for filename in os.listdir(output_directory):  # Iterating through each file in the directory
        file_path = os.path.join(output_directory, filename)  # Constructing the full path of the file
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Deleting the file or symlink
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Deleting the directory and its contents
        except Exception as e:
            logging.error(f'Failed to delete {file_path}. Reason: {e}')  # Logging any errors encountered

    
def download_video(url, quality='best', output_directory=OUTPUT_DIRECTORY):
    """
    Downloads a video from the provided URL at the specified quality.

    Parameters:
    - url (str): The URL of the video to be downloaded.
    - quality (str, optional): The desired quality of the video. Defaults to 'best'.
    - output_directory (str, optional): The directory where the video will be saved. Defaults to OUTPUT_DIRECTORY.

    Returns:
    - tuple: The file path and file name of the downloaded video.
    """
    clear_downloads_folder(output_directory)  # Clearing the downloads folder
    # Defining format options based on the desired quality
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

    # Defining options for yt_dlp
    ydl_opts = {
        'format': format_option,
        'outtmpl': f'{output_directory}/%(playlist)s/%(title)s.%(ext)s',  # Template for output file name
        'ffmpeg_location': FFMPEG_LOCATION,  # Specifying the location of ffmpeg binary
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',  # Using FFmpeg for post-processing
            'preferedformat': 'mp4',  # Preferred format is mp4
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Creating a YoutubeDL object with the specified options
        info_dict = ydl.extract_info(url, download=False)  # Extracting video info without downloading
        file_path = ydl.prepare_filename(info_dict)  # Preparing the file name
        error_code = ydl.download([url])  # Downloading the video
        video_title = info_dict.get('title', 'video')  # Getting the video title
        file_name = f'{video_title}.mp4'  # Constructing the file name
        print(error_code) # TODO: should return none if download works otherwise an int. Need to check this
        return file_path, file_name  # Returning the file path and file name
    

def download_audio(url, audio_quality='192', output_directory=OUTPUT_DIRECTORY):
    """
    Downloads the audio from the provided URL at the specified quality.

    Parameters:
    - url (str): The URL of the video from which audio will be extracted.
    - audio_quality (str, optional): The desired quality of the audio. Defaults to '192'.
    - output_directory (str, optional): The directory where the audio file will be saved. Defaults to OUTPUT_DIRECTORY.

    Returns:
    - tuple: The file path and file name of the downloaded audio.
    """
    clear_downloads_folder(output_directory)  # Clearing the downloads folder

    # Defining options for yt_dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Selecting the best available audio format
        'outtmpl': f'{output_directory}/%(title)s.%(ext)s',  # Template for output file name
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Using FFmpeg to extract audio
            'preferredcodec': 'mp3',  # Preferred audio codec is mp3
            'preferredquality': audio_quality,  # Setting the preferred audio quality
        }],
        'ffmpeg_location': FFMPEG_LOCATION,  # Specifying the location of ffmpeg binary
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Creating a YoutubeDL object with the specified options
        info_dict = ydl.extract_info(url, download=False)  # Extracting video info without downloading
        error_code =ydl.download([url])  # Downloading the audio
        audio_title = info_dict.get('title', 'audio')  # Getting the audio title
        file_name = f'{audio_title}.mp3'  # Constructing the file name
        file_path = f'{output_directory}/{file_name}'  # Constructing the file path
        print(error_code) # TODO: should return none if download works otherwise an int. Need to check this
        return file_path, file_name  # Returning the file path and file name


def get_video_info(url):
    """
    Retrieves the title and thumbnail URL of the video at the provided URL.

    Parameters:
    - url (str): The URL of the video.

    Returns:
    - tuple: The title and thumbnail URL of the video.
    """
    # Defining options for yt_dlp
    ydl_opts = {
        'quiet': True,  # Suppressing console output
        'extract_flat': False,  # Enabling detailed info extraction
        'force_generic_extractor': False,  # Allowing specific extractors
        'noplaylist': True,  # Ensuring only single video info is retrieved, not playlist info
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Creating a YoutubeDL object with the specified options
        result = ydl.extract_info(url, download=False)  # Extracting video info without downloading
        video = result['entries'][0] if 'entries' in result else result  # Handling both video and playlist cases
        video_title = video.get('title', None)  # Getting the video title
        thumbnail_url = video.get('thumbnail', None)  # Getting the thumbnail URL
        return video_title, thumbnail_url  # Returning the video title and thumbnail URL


if __name__ == "__main__":
    setup_logging()

