#!/usr/bin/env python
# coding: utf-8

"""
This module provides functionality for extracting 
transcripts from YouTube videos given a channel's
username or ID. It fetches the upload playlist ID 
of a channel, retrieves all videos from this
playlist, and attempts to fetch the transcript for 
each video using the YouTube Transcript API.
The collected data, including video titles, URLs, 
and transcripts, is then saved as a JSON file.

Usage requires a valid YouTube Data API key and
either the username or the ID of a YouTube channel.
The module defines functions for fetching playlist 
IDs, retrieving playlist items, and saving video
information to JSON. It's designed to be run as a 
script, with example usage that fetches and saves
video information from a specified channel.

Authors: Mark Daniel, Amit Peled 
Date: 2024-02-20
"""

import requests

def get_channel_upload_playlist_id_by_username(yt_data_api_key, username):
    """
    Fetches the upload playlist ID for a given YouTube channel username.
    
    Parameters:
    - api_key: The YouTube Data API key.
    - username: The username of the YouTube channel.
    
    Returns:
    - The upload playlist ID as a string.
    """
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    url=f"{base_url}?part=contentDetails&forUsername={username}&key={yt_data_api_key}"
    response = requests.get(url, timeout=600)
    data = response.json()
    if data['items']:
        return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return None

def get_channel_upload_playlist_id_by_channelid(yt_data_api_key, channel_id):
    """
    Fetches the upload playlist ID for a given YouTube channel ID.
    
    Parameters:
    - api_key: The YouTube Data API key.
    - channel_id: The ID of the YouTube channel.
    
    Returns:
    - The upload playlist ID as a string.
    """
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    url = f"{base_url}?part=contentDetails&id={channel_id}&key={yt_data_api_key}"
    response = requests.get(url, timeout=600)
    data = response.json()
    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_playlist_items(yt_data_api_key, playlist_id):
    """
    Retrieves all items in a given YouTube playlist.
    
    Parameters:
    - api_key: The YouTube Data API key.
    - playlist_id: The ID of the playlist from which to fetch items.
    
    Returns:
    - A list of items (videos) from the playlist.
    """
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    url = (
        f"{base_url}?part=snippet,contentDetails"
        f"&maxResults=50&playlistId={playlist_id}&key={yt_data_api_key}"
    )
    items = []
    while True:
        response = requests.get(url,timeout=600)
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
