"""
Unit tests for the indexing module.
"""
import unittest

from main import indexing


def is_list_of_dicts(data):
    """Helper that checks if the data is a list of dictionaries."""
    return isinstance(data, list) and all(isinstance(item, dict) for item in data)


class TestIndexingFuctions(unittest.TestCase):
    """
    Unit tests for the indexing module. Uses test_data for load validation 
    and temp files for output validation.
    """

    def test_smoke_transcript_load(self):
        """Test that transcripts are loaded into a list of json objects (dicts)"""
        test_jsons = indexing.load_json_transcripts("./tests/test_data")
        self.assertTrue(is_list_of_dicts(test_jsons))

    def test_document_creation(self):
        """Test to make sure documents are created with the proper metadata"""
        expected_metadata_keys = set([
            "episode_title",
            "episode_number",
            "episode_summary",
            "youtube_link",
            "timestamp",
        ])
        test_jsons = indexing.load_json_transcripts("./tests/test_data")
        test_docs = indexing.parse_into_documents(test_jsons)
        for doc in test_docs:
            self.assertEqual(expected_metadata_keys, set(doc.metadata))




if __name__ == '__main__':
    unittest.main()
