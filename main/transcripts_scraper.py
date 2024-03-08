#!/usr/bin/env python
# coding: utf-8

"""
This module provides functionality for extracting transcripts from YouTube videos given a channel's username or ID.
It fetches the upload playlist ID of a channel, retrieves all videos from this playlist, and attempts to fetch
the transcript for each video using the YouTube Transcript API. The collected data, including video titles, URLs,
and transcripts, is then saved as a JSON file.

Usage requires a valid YouTube Data API key and either the username or the ID of a YouTube channel. The module
defines functions for fetching playlist IDs, retrieving playlist items, and saving video information to JSON.
It's designed to be run as a script, with example usage that fetches and saves video information from a specified channel.
"""

import requests
import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import json

def get_channel_upload_playlist_id_by_username(api_key, username):
    """
    Fetches the upload playlist ID for a given YouTube channel username.
    
    Parameters:
    - api_key: The YouTube Data API key.
    - username: The username of the YouTube channel.
    
    Returns:
    - The upload playlist ID as a string.
    """
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    url = f"{base_url}?part=contentDetails&forUsername={username}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_channel_upload_playlist_id_by_channelid(api_key, channel_id):
    """
    Fetches the upload playlist ID for a given YouTube channel ID.
    
    Parameters:
    - api_key: The YouTube Data API key.
    - channel_id: The ID of the YouTube channel.
    
    Returns:
    - The upload playlist ID as a string.
    """
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    url = f"{base_url}?part=contentDetails&id={channel_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_playlist_items(api_key, playlist_id):
    """
    Retrieves all items in a given YouTube playlist.
    
    Parameters:
    - api_key: The YouTube Data API key.
    - playlist_id: The ID of the playlist from which to fetch items.
    
    Returns:
    - A list of items (videos) from the playlist.
    """
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    url = f"{base_url}?part=snippet,contentDetails&maxResults=50&playlistId={playlist_id}&key={api_key}"
    items = []
    while True:
        response = requests.get(url)
        data = response.json()
        items.extend(data["items"])
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
        url = f"{url}&pageToken={next_page_token}"
    return items

def save_video_information_to_json(video_information, file_path):
    """
    Saves the video information to a JSON file at the specified path.
    
    Parameters:
    - video_information: The video information to save (as a DataFrame).
    - file_path: The path where the JSON file will be saved.
    """
    video_information.to_json(file_path, orient='records', lines=True)

if __name__ == "__main__":
    api_key = "AIzaSyCZkMX4lpsmBLzaVQRBbkVXc8jUHt8mE18"  ########MARK FOR REMOVAL#######
    channel_id="UC2D2CMWXMOVWx7giW1n3LIg"
    upload_playlist_id = get_channel_upload_playlist_id_by_channelid(api_key, channel_id)
    playlist_items = get_playlist_items(api_key, upload_playlist_id)
    dfs = []
    for item in playlist_items:
        video_id = item["contentDetails"]["videoId"]
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            transcript = json.dumps(YouTubeTranscriptApi.get_transcript(video_id))
        except Exception as e:
            print(f"Error getting transcript for video {video_id}: {e}")
            transcript = "N/A"
        df_video = pd.DataFrame({
            'Video Title': [video_title], 
            'Video URL': [video_url], 
            'Transcript': [transcript]
        })
        dfs.append(df_video)
    df_combined = pd.concat(dfs, ignore_index=True)
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    json_file_path = os.path.join(desktop_path, "youtube_videos.json")
    save_video_information_to_json(df_combined, json_file_path)
    print(f"\nVideo information has been saved to '{json_file_path}'.")