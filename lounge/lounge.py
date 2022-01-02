import pytube
from pytube import YouTube
from pytube import Stream
import os
import glob
import ffmpeg

class YoutubeVideo:
    def __init__(self, search_term):
        self.search_term = str(search_term)
        try:
            self.yt_video: pytube.YouTube = pytube.Search(search_term).results[0]
        except:
            self.yt_video = None
            pass
        self.file_path = ""

    def start_download(self):
        target_stream = self.yt_video.streams.get_audio_only()

        file_name = "{0}.mp4".format(self.yt_video.video_id)
        file_name = "downloads/" + file_name
        print(file_name)

        if os.path.isfile(file_name):
            print(file_name)
            self.file_path = file_name
        else:
            self.file_path = file_name
            target_stream.download(output_path="", filename=file_name, max_retries=1)