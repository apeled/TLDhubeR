"""
Unit tests for the indexing module.
"""

import unittest
from unittest.mock import Mock, patch

from main import indexing


def is_list_of_dicts(data):
    """Helper that checks if the data is a list of dictionaries."""
    return isinstance(data, list) and all(isinstance(item, dict) for item in data)


class TestIndexingFuctions(unittest.TestCase):
    """
    Unit tests for the indexing module. Uses test_data for load validation
    and mocks components with API responses for output validation.
    """

    # Define globals for use in multiple tests
    test_jsons = indexing.load_json_transcripts("./tests/test_data")
    test_docs = indexing.parse_into_documents(test_jsons)

    def test_smoke_transcript_load(self, test_jsons=test_jsons):
        """Test that transcripts are loaded into a list of json objects (dicts)"""
        self.assertTrue(is_list_of_dicts(test_jsons))

    def test_document_creation(self, test_docs=test_docs):
        """Test to make sure documents are created with the proper metadata"""
        expected_metadata_keys = set(
            [
                "episode_title",
                "episode_number",
                "episode_summary",
                "youtube_link",
                "timestamp",
            ]
        )
        for doc in test_docs:
            self.assertEqual(expected_metadata_keys, set(doc.metadata))

    def test_simple_search(self, test_docs=test_docs):
        """
        Test to ensure semantic vector searching is able to find
        an obvious match. This is essentially a one-shot test that our llama-index
        objects are created with the correct arguments and that the embedding
        model of the query engine matches the embeddings of the text nodes.
        """
        expected_text = (
            "Conclusion: indexing.py seems to work. Now go take a break, scientist!"
        )
        test_engine = indexing.get_simple_hube_engine(test_docs)
        retrieved_nodes = test_engine.query("Does indexing.py work?").source_nodes
        top_match_text = retrieved_nodes[0].text
        self.assertEqual(top_match_text, expected_text)

    def test_process_documents(self, test_docs=test_docs):
        """
        This function tests to make sure that the read and write functionality
        of process_documents is working, that there are no indexing errors, etc.
        """
        expected_nodes = indexing.unpickle_nodes("./tests/test_data")
        # Mock IngestionPipeline to load test_nodes
        mock_pipeline = Mock(indexing.IngestionPipeline)
        mock_pipeline.run.return_value = expected_nodes
        # Mock dump_object (test writing the mocked nodes to file)
        mock_dump_object = Mock(indexing.dump_object)
        mock_dump_object.side_effect = indexing.dump_object(
            expected_nodes,
            filename="test_output.pkl",
            base_path="./tests/test_data/test_output",
        )
        # Use the mocks in a test. Takes 60 seconds to run
        indexing.process_documents(
            test_docs, pipeline=mock_pipeline, dump_object=mock_dump_object
        )

        # Assert expectations on the mock
        mock_pipeline.run.assert_called_once_with(documents=test_docs)

        # Assert that the correct nodes were written
        written_nodes = indexing.unpickle_nodes("./tests/test_data/test_output")
        self.assertEqual(written_nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
