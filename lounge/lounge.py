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
            self.yt_video = pytube.Search(search_term).results[0]
        except:
            pass
        self.file_path = ""

    def start_download(self):
        streams = self.yt_video.fmt_streams
        target_stream: Stream = None

        print(streams)

        for stream in streams:
            if stream.type == 'audio' and stream.mime_type == 'audio/mp4':
                target_stream = stream
                break
        else:
            target_stream = streams[0]

        file_name = "{0}.mp4".format(self.yt_video.video_id)
        file_name = "downloads/" + file_name
        print(file_name)

        if os.path.isfile(file_name):
            print(file_name)
            self.file_path = file_name
        else:
            self.file_path = file_name
            target_stream.download(output_path="", filename=file_name, max_retries=1)