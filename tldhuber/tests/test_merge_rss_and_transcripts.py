"""
This module contains unit tests for the merge_rss_and_transcripts function. It tests
various scenarios including successful data merging, handling empty YouTube playlists,
and cases where there are more RSS entries than YouTube videos. The tests ensure that
the function behaves as expected under different conditions by mocking external dependencies
and verifying the function's output.
"""

import unittest
from unittest.mock import patch, mock_open

import pandas as pd

from tldhuber.utils.merge_rss_and_transcripts import merge_rss_and_transcripts

class TestMergeRSSAndTranscripts(unittest.TestCase):
    """Test cases for the merge_rss_and_transcripts function."""

    def setUp(self):
        """Set up mock data for testing, including mock RSS data and YouTube playlist items."""
        self.mock_rss_data = pd.DataFrame({
            'Title': ['Episode 1', 'Episode 2'],
            'Publication Date': ['2023-01-01', '2023-01-02'],
            'Summary': ['Summary 1', 'Summary 2'],
            'Enclosure Link': ['http://example.com/1', 'http://example.com/2']
        })

        self.mock_playlist_items = [
            {"contentDetails": {"videoId": "12345"}, "snippet": {"title": "Video 1"}},
            {"contentDetails": {"videoId": "67890"}, "snippet": {"title": "Video 2"}}
        ]

    @patch('main.merge_rss_and_transcripts.get_playlist_items')
    @patch('main.merge_rss_and_transcripts.get_channel_upload_playlist_id_by_channelid',
           return_value="some_playlist_id")
    @patch('main.merge_rss_and_transcripts.scrape_rss_data')
    def test_merge_success(self, mock_scrape_rss_data, _, mock_get_playlist_items):
        """Test successful merging of RSS and YouTube data."""
        mock_scrape_rss_data.return_value = self.mock_rss_data
        mock_get_playlist_items.return_value = self.mock_playlist_items

        with patch('builtins.open',
                   new_callable=mock_open) as mocked_open,patch('json.dump') as mocked_json_dump:
            merge_rss_and_transcripts('fake_api_key', 'fake_channel_id', 'fake_rss_feed_url')

            self.assertEqual(mocked_open.call_count, len(self.mock_playlist_items))
            mocked_json_dump.assert_called()

    @patch('main.merge_rss_and_transcripts.get_playlist_items', return_value=[])
    @patch('main.merge_rss_and_transcripts.get_channel_upload_playlist_id_by_channelid',
           return_value="some_playlist_id")
    @patch('main.merge_rss_and_transcripts.scrape_rss_data', return_value=pd.DataFrame({
            'Title': ['Episode 1', 'Episode 2'],
            'Publication Date': ['2023-01-01', '2023-01-02'],
            'Summary': ['Summary 1', 'Summary 2'],
            'Enclosure Link': ['http://example.com/1', 'http://example.com/2']
        }))
    # def test_empty_youtube_playlist(self, _, __, ___):
    #     """Test the behavior when the YouTube playlist is empty."""
    #     with patch("builtins.open", mock_open()) as mock_file_open, patch("json.dump"):
    #         merge_rss_and_transcripts('fake_api_key', 'fake_channel_id', 'fake_rss_feed_url')

    #         mock_file_open.assert_not_called()

    @staticmethod
    @patch('main.merge_rss_and_transcripts.scrape_rss_data')
    @patch('main.merge_rss_and_transcripts.get_playlist_items', return_value=[
        {"contentDetails": {"videoId": "12345"}, "snippet": {"title": "Video 1"}},
        {"contentDetails": {"videoId": "67890"}, "snippet": {"title": "Video 2"}}
    ])
    @patch('main.merge_rss_and_transcripts.get_channel_upload_playlist_id_by_channelid',
           return_value="some_playlist_id")
    def test_more_rss_entries_than_youtube_videos(_, mock_get_playlist_items,
    mock_scrape_rss_data):
        """Test processing when there are more RSS entries than YouTube videos."""
        mock_rss_data_extended = pd.DataFrame({
            'Title': ['Episode 1', 'Episode 2', 'Episode 3'],
            'Publication Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Summary': ['Summary 1', 'Summary 2', 'Summary 3'],
            'Enclosure Link': ['http://example.com/1', 'http://example.com/2',
                               'http://example.com/3']
        })
        mock_scrape_rss_data.return_value = mock_rss_data_extended

        with patch("builtins.open", mock_open()) as mock_file_open, patch("json.dump"):
            merge_rss_and_transcripts('fake_api_key', 'fake_channel_id', 'fake_rss_feed_url')

            assert mock_file_open.call_count == len(mock_get_playlist_items.return_value)

if __name__ == '__main__':
    unittest.main()
