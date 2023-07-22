from googleapiclient.discovery import build
import os
from datetime import datetime


def get_channel_name_by_id(youtube_client, channel_name):
    request = youtube_client.channels().list(
        part="id",
        forUsername=channel_name
    )
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['id']


def get_channel_metrics(youtube_client, channel_id):
    request = youtube_client.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]
    else:
        raise Exception("Error fetching channel metrics.")


def engagement_rating(likes, views):
    return (int(likes)/int(views))


def get_top_performing_videos(youtube_client, channel_id):
    request = youtube_client.search().list(
        part="id",
        channelId=channel_id,
        order="viewCount",
        type="video",
        maxResults=5
    )
    response = request.execute()

    top_performing_videos = []
    vids = []
    for item in response['items']:
        dict1 = {}
        dict2 = {}
        req = youtube_client.videos().list(
            part="id,snippet,statistics",
            id=item['id']['videoId']
        )
        res = req.execute()
        dict1['id'] = res["items"][0]["id"]
        dict2['id'] = res["items"][0]["id"]
        dict2["engagementRate"] = engagement_rating(
            res['items'][0]['statistics']["likeCount"], res['items'][0]['statistics']["viewCount"])
        dict1["viewCount"] = res['items'][0]['statistics']["viewCount"]
        dict1["publishedAt"] = res["items"][0]["snippet"]["publishedAt"]
        top_performing_videos.append(dict1)
        vids.append(dict2)
    return (vids, top_performing_videos)


def calculate_publishing_frequency(channel_metrics):

    if "publishedAt" in channel_metrics["snippet"]:
        published_month = int(
            channel_metrics["snippet"]["publishedAt"].split("-")[1])
        published_year = int(
            channel_metrics["snippet"]["publishedAt"].split("-")[0])
        current_month = int(get_current_time().split("-")[1])
        current_year = int(get_current_time().split("-")[0])
        return round(int(channel_metrics["statistics"]["videoCount"])/((current_year-published_year-2)*12 + current_month + 12-published_month))


def get_optimal_publishing_time(top_videos):
    video_views_by_hour = {}
    for video in top_videos:
        publishing_time = int(
            video["publishedAt"].split("T")[1][:2])
        video_views_by_hour[publishing_time] = video_views_by_hour.get(
            publishing_time, 0) + int(video["viewCount"])

    optimal_publishing_time_slot = max(
        video_views_by_hour, key=video_views_by_hour.get)

    if 0 <= optimal_publishing_time_slot < 4:
        return "0-4"
    elif 4 <= optimal_publishing_time_slot < 8:
        return "4-8"
    elif 8 <= optimal_publishing_time_slot < 12:
        return "8-12"
    elif 12 <= optimal_publishing_time_slot < 16:
        return "12-16"
    elif 16 <= optimal_publishing_time_slot < 20:
        return "16-20"
    else:
        return "20-24"


def get_current_time():
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    return current_time


def analyze_youtube_channel(youtube_client, channel_name):
    # Getting channel id
    channel_id = get_channel_name_by_id(youtube_client, channel_name)

    # Getting channel metrics
    channel_metrics = get_channel_metrics(youtube_client, channel_id)

    # Getting Top Performing Videos &
    # Data to calculate other things
    vids, top_performing_videos = get_top_performing_videos(
        youtube_client, channel_id)

    subscriber_count = int(
        channel_metrics["statistics"].get("subscriberCount", 0))
    video_views = int(channel_metrics["statistics"].get("viewCount", 0))

    # Getting publishing frequescy
    publishing_frequency = calculate_publishing_frequency(channel_metrics)

    # Getting optimal publishing time
    optimal_publishing_time = get_optimal_publishing_time(
        top_performing_videos)

    # Making result
    analysis_results = {
        "topPerformingVideos": vids,
        "subscriberCount": subscriber_count,
        "videoViews": video_views,
        "publishingFrequency": publishing_frequency,
        "optimalPublishingTime": optimal_publishing_time,
    }

    # Returning Result
    return analysis_results


if __name__ == '__main__':
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    API_KEY = "AIzaSyAPWKKinikTNeUHdh3NUXASATssq_FD1xQ"  # Change this to your own key

    # Build the YouTube API client
    api_service_name = "youtube"
    api_version = "v3"
    youtube_client = build(api_service_name, api_version, developerKey=API_KEY)
    channel_name = "AdobeCreativeCloud"

    # Starting main function
    analysis_results = analyze_youtube_channel(youtube_client, channel_name)

    # Printing main function result
    print(analysis_results)
