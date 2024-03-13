"""
Unit tests for the YouTube video transcript extraction module.

This test suite provides a series of unit tests for the transcript_scraper module.
It tests fetching the upload playlist ID, retrieving playlist items, and saving video information
to a JSON file. The tests use mocking to simulate API responses, so that that no actual network
requests are made.
"""

import unittest
from unittest.mock import patch
import os
import json
import pandas as pd

from tldhuber.utils.transcripts_scraper import (get_channel_upload_playlist_id_by_username,
                                      get_channel_upload_playlist_id_by_channelid,
                                      get_playlist_items, save_video_information_to_json)


class TestTranscriptsScraper(unittest.TestCase):
    """
    Test suite for the transcripts_scraper module that extracts YouTube video transcripts.

    This class tests all the functions defined in transcripts_scraper module,
    including fetching upload playlist IDs, retrieving playlist items, and saving video
    information to JSON.
    """

    @patch('requests.get')
    def test_get_channel_upload_playlist_id_by_username(self, mock_get):
        """
        Test fetching the upload playlist ID using a YouTube channel username.
        """
        mock_get.return_value.json.return_value = {
            "items": [
                {
                    "contentDetails": {
                        "relatedPlaylists": {
                            "uploads": "UPLOAD_PLAYLIST_ID"
                        }
                    }
                }
            ]
        }
        api_key = "dummy_api_key"
        username = "dummy_username"
        result = get_channel_upload_playlist_id_by_username(api_key, username)
        self.assertEqual(result, "UPLOAD_PLAYLIST_ID")

    @patch('requests.get')
    def test_get_channel_upload_playlist_id_by_channelid(self, mock_get):
        """
        Test fetching the upload playlist ID using a YouTube channel ID.
        """
        mock_get.return_value.json.return_value = {
            "items": [
                {
                    "contentDetails": {
                        "relatedPlaylists": {
                            "uploads": "UPLOAD_PLAYLIST_ID"
                        }
                    }
                }
            ]
        }
        api_key = "dummy_api_key"
        channel_id = "dummy_channel_id"
        result = get_channel_upload_playlist_id_by_channelid(api_key, channel_id)
        self.assertEqual(result, "UPLOAD_PLAYLIST_ID")

    @patch('requests.get')
    def test_get_playlist_items(self, mock_get):
        """
        Test retrieving all items from a YouTube playlist.
        """
        mock_get.return_value.json.side_effect = [
            {"items": ["video1", "video2"], "nextPageToken": "token"},
            {"items": ["video3"]}
        ]
        api_key = "dummy_api_key"
        playlist_id = "dummy_playlist_id"
        result = get_playlist_items(api_key, playlist_id)
        self.assertEqual(result, ["video1", "video2", "video3"])

    def test_save_video_information_to_json(self):
        """
        Test saving video information to a JSON file.
        """
        video_information = pd.DataFrame({
            'Video Title': ['Title 1'],
            'Video URL': ['http://example.com'],
            'Transcript': ['This is a transcript.']
        })
        file_path = "test_output.json"
        save_video_information_to_json(video_information, file_path)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)  # Deserialize JSON content to a Python object
            self.assertEqual(content['Video URL'], 'http://example.com')
            self.assertEqual(content['Video Title'], 'Title 1')
            self.assertEqual(content['Transcript'], 'This is a transcript.')

        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
