from pytube import YouTube
from pytube import Stream
import os
import ffmpeg

class YoutubeVideo:
    def __init__(self, url):
        self.url = str(url)
        self.yt_video: YouTube = YouTube(self.url)
        self.file_path = ""

    def start_download(self):
        streams = self.yt_video.fmt_streams
        target_stream: Stream = None

        for stream in streams:
            if stream.type == 'audio':
                target_stream = stream
                break
        else:
            target_stream = streams[0]

        file_name = "{0}.mp4".format(self.yt_video.title)

        new_file_name = ""
        for file_name_chunk in file_name.split(' '):
            new_file_name += '_' + file_name_chunk
        file_name = new_file_name

        new_file_name = ""
        for file_name_chunk in file_name.split('&'):
            new_file_name += '_' + file_name_chunk
        file_name = "Downloads/" + new_file_name
        print(file_name)

        if os.path.isfile(file_name):
            print(file_name)
            self.file_path = file_name
        else:
            self.file_path = file_name
            target_stream.download(output_path="", filename=file_name, max_retries=1)