import ntpath

from pytube import YouTube
from moviepy.editor import *


class app_controller:
 @classmethod
 def download_and_convert(cls,video_link):
     path_mp4=app_controller.download_mp4(video_link)
     path_mp3=app_controller.convert_mp4_to_mp3(path_mp4)
     return path_mp3

 @classmethod
 def download_mp4(cls,video_link):
    # YouTube('https://youtu.be/9bZkp7q19f0').streams.first().download()
    yt = YouTube(video_link)
    mp4_file = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().download()
    return mp4_file

 @classmethod
 def convert_mp4_to_mp3(cls,video_path):

    mp3_file = ntpath.basename(video_path).replace(".mp4",".mp3")
    videoclip = VideoFileClip(video_path)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)
    audioclip.close()
    videoclip.close()
    return os.path.dirname(video_path)+"\\"+mp3_file