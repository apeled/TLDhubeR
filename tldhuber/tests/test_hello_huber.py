"""
Unit tests for the Streamlit app, focusing on embedding YouTube videos
correctly and handling API responses.

This test suite aims to ensure the core functionalities of the Streamlit
application are working as expected, particularly in areas concerning data
handling, query processing, and YouTube link manipulation. It leverages
mocking to isolate tests from external dependencies, allowing for efficient
and focused validation of the application logic.
"""

import unittest
from unittest.mock import patch, MagicMock

from tldhuber.hello_huber import (read_markdown_file,
                                  load_data,
                                  set_up_engine,
                                  get_mid_video_link,
                                  extract_metadata, clear_session_state)

class TestHelloHuber(unittest.TestCase):
    """
    A collection of unit tests designed to verify the functionality of
    the hello_huber Streamlit application.
    """

    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data='Test Markdown Content')
    def test_read_markdown_file(self, _):
        """
        Test the `read_markdown_file` function to ensure it correctly reads
        and returns the content of a markdown file.
        """
        content = read_markdown_file('fake_path.md')
        self.assertEqual(content, 'Test Markdown Content')

    @patch('tldhuber.hello_huber.load_index_from_storage')
    @patch('tldhuber.hello_huber.StorageContext.from_defaults')
    def test_load_data(self, mock_storage_context, mock_load_index):
        """
        Test the `load_data` function to verify that the podcast data is
        successfully loaded and indexed for querying.
        """
        mock_load_index.return_value = MagicMock()
        mock_storage_context.return_value = MagicMock()
        result = load_data()
        self.assertIsNotNone(result)

    @patch('tldhuber.hello_huber.VectorIndexRetriever')
    def test_set_up_engine(self, _):
        """
        Test the `set_up_engine` function to ensure a query engine is properly
        initialized with the loaded podcast data index.
        """
        mock_index = MagicMock()
        engine = set_up_engine(mock_index)
        self.assertIsNotNone(engine)

    def test_get_mid_video_link(self):
        """
        Test the `get_mid_video_link` function to ensure it correctly modifies
        a YouTube URL to start playback at a specified timestamp.
        """
        original_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        expected_link = "https://youtu.be/dQw4w9WgXcQ?t=60"
        modified_link = get_mid_video_link(original_link, 60)
        self.assertEqual(modified_link, expected_link)

    @patch('tldhuber.hello_huber.set_up_engine')
    def test_extract_metadata(self, mock_set_up_engine):
        """
        Test the `extract_metadata` function to verify that it correctly extracts
        and transforms metadata from the query response, specifically adjusting
        YouTube links to include the appropriate start time.
        """
        mock_engine = MagicMock()
        mock_engine.query.return_value = MagicMock(source_nodes=[
            MagicMock(metadata={'youtube_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                                'timestamp': 60})
        ])
        mock_set_up_engine.return_value = mock_engine

        metadata = extract_metadata(mock_engine.query(""))
        self.assertEqual(len(metadata), 1)
        self.assertIn('?t=60', metadata[0]['youtube_link'])

    @patch('tldhuber.hello_huber.st.session_state', new_callable=dict)
    def test_clear_session_state(self, mock_session_state):
        """Ensure the session state is cleared correctly."""
        mock_session_state['key1'] = 'value1'
        mock_session_state['key2'] = 'value2'
        clear_session_state()
        self.assertEqual(len(mock_session_state), 0,
                         "Session state should be empty after clearing.")

    @patch('tldhuber.hello_huber.load_index_from_storage', return_value=MagicMock())
    @patch('tldhuber.hello_huber.StorageContext.from_defaults', return_value=MagicMock())
    def test_load_data_failure(self, _, mock_load_index):
        """Test load_data behavior when indexing fails."""
        mock_load_index.side_effect = Exception("Indexing failed")
        with self.assertRaises(Exception, msg="Should raise an exception for failed indexing"):
            load_data()

    def test_extract_metadata_with_varied_data(self):
        """Test metadata extraction with various data structures."""
        query_response = MagicMock()
        query_response.source_nodes = [
            MagicMock(metadata={'youtube_link': 'https://www.youtube.com/watch?v=example1',
                                'timestamp': 30}),
            MagicMock(metadata={'youtube_link': 'https://www.youtube.com/watch?v=example2',
                                'timestamp': 0})
        ]
        metadata = extract_metadata(query_response)
        self.assertEqual(len(metadata), 2, "Should handle multiple metadata entries.")
        self.assertIn('?t=30', metadata[0]['youtube_link'])
        self.assertIn('youtu.be/example2', metadata[1]['youtube_link'],
                      "Should handle timestamp at 0 correctly.")

    def test_get_mid_video_link_edge_cases(self):
        """Test modifying YouTube links for edge case timestamps."""
        link_no_change = get_mid_video_link("https://www.youtube.com/watch?v=example", 0)
        self.assertIn('youtu.be/example', link_no_change,
                      "Link should be modified correctly even for timestamp 0.")

if __name__ == '__main__':
    unittest.main()
