import ntpath
from pytube import YouTube
from moviepy.editor import *
from googleapiclient.discovery import build


class app_controller:
    """
    A class that provides data to the view.
    """
    # A flag that marker if the user need to choose a video from the suggestions.
    num_flag = False
    # A list of the links of the suggestions.
    lst_results = []

    @classmethod
    def download_and_convert(cls,video_link):
        """
        A function that download video file of video_link and convert to mp3 file
        :param video_link: A link of a video in youtube
        :return: The path of the mp3 file
        """
        path_mp4 = app_controller.download_mp4(video_link)
        path_mp3 = app_controller.convert_mp4_to_mp3(path_mp4)
        return path_mp3

    @classmethod
    def download_mp4(cls, video_link):
        """
        A function that download video file of video_link
        :param video_link: A link of a video in youtube
        :return: The path of the local mp4 file
        """
        yt = YouTube(video_link)
        mp4_file = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download()
        return mp4_file

    @classmethod
    def convert_mp4_to_mp3(cls, video_path):
        """
        A function that convert a mp4 file to mp3 file
        :param video_path: A path of the local mp4 file
        :return: The path of the mp3 file
        """
        mp3_file = ntpath.basename(video_path).replace(".mp4", ".mp3")
        videoclip = VideoFileClip(video_path)
        audioclip = videoclip.audio
        audioclip.write_audiofile(mp3_file)
        audioclip.close()
        videoclip.close()
        return os.path.dirname(video_path)+"\\"+mp3_file


    @classmethod
    def search_by_keyword(cls, name_video):
        """
        A function that search name_video in youtube and return the suggestions
        :param name_video: A value to search
        :return: a dict with the suggestions - name and link
        """

        api_key = ''
        youtube = build('youtube', 'v3', developerKey=api_key)
        req = youtube.search().list(q=name_video, part='snippet', type='video')
        res = req.execute()
        dict_video = {}
        for video in res['items']:
            dict_video[video['id']['videoId']] = video['snippet']['title']
        return dict_video
