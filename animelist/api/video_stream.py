from pytube import YouTube
from pytube.exceptions import PytubeError, VideoUnavailable


def stream_video(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        title = yt.title
        views = yt.views
        released = yt.publish_date
        thumbnail = yt.thumbnail_url

        # Get the highest quality adaptive stream
        stream = yt.streams.filter(adaptive=True, file_extension='mp4').first()

        if stream:
            # Get the stream URL
            stream_url = stream.url
            return [{'stream': stream_url, 'available': True, 'title': title, 'views': views,
                     'released': released, 'thumbnail': thumbnail}]
        else:
            # If no suitable stream is found
            print("No suitable stream found.")
            return [{'available': False}]

    except VideoUnavailable:
        # Handle video unavailable error
        print("The video is unavailable.")
        return [{'available': False}]

    except PytubeError as e:
        # Handle Pytube-specific errors
        print(f"PytubeError: {e}")
        return [{'available': False}]

    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return [{'available': False}]

