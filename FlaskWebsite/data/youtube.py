# pip install youtube_transcript_api
# pip install google-api-python-client

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import datetime

def get_captions(video_id):
    api_key = "AIzaSyBdGMvQ4K0JNQcfOiK2_KpWeGDEEkEc8hI"
    # the API key that you generate on Google Developers
    youtube = build("youtube", "v3", developerKey=api_key)
    # create a YouTube Data API v.3 object
    srt = YouTubeTranscriptApi.get_transcript(video_id, languages=["fr"])
    # get the captions data
    transcriptions = []
    time_caption = []
    for i in srt:
        transcriptions.append(i["text"])
        time = datetime.timedelta(seconds=round(i["start"]))
        time_caption.append(time)

    df = pd.DataFrame({"time_caption": time_caption, "transcript": transcriptions})

    time_captions = list(pd.DataFrame(df.resample("T", on="time_caption"))[0])
    transcriptions = list(
        pd.DataFrame(df.resample("T", on="time_caption").agg({"transcript": " ".join}))[
            "transcript"
        ]
    )

    request = youtube.videos().list(part="contentDetails,snippet", id=video_id)
    response = request.execute()
    # make a request to the data of the video and execute it
    # the resulting response is a dictionary with lots of metadata of the video
    channel_id = [response["items"][0]["snippet"]["channelId"]] * len(transcriptions)
    video_description = [response["items"][0]["snippet"]["description"]] * len(
        transcriptions
    )
    upload_date = [
        response["items"][0]["snippet"]["publishedAt"]
        .replace("T", " ")
        .replace("Z", "")
    ] * len(transcriptions)
    channel_id = [channel_id] * len(transcriptions)
    channel_title = [response["items"][0]["snippet"]["channelTitle"]] * len(
        transcriptions
    )
    video_id = [response["items"][0]["id"]] * len(transcriptions)
    duration = [
        response["items"][0]["contentDetails"]["duration"][2:]
        .replace("M", ":")
        .replace("S", "")
    ] * len(transcriptions)
    video_title = [response["items"][0]["snippet"]["title"]] * len(transcriptions)

    df = pd.DataFrame(
        {
            "channel_title": channel_title,
            "channel_id": channel_id,
            "video_title": video_title,
            "video_id": video_id,
            "video_description": video_description,
            "upload_date": upload_date,
            "duration": duration,
            "time_caption": time_captions,
            "transcript": transcriptions,
        }
    )
    # create the dataframe

    return df
