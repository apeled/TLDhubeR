"""
Unit tests for the streamlit app. This file tests that we are embedding
youtube videos correctly and that we are properly handling api responses.
"""

from unittest.mock import patch

from tldhuber.hello_huber import get_mid_video_link, load_data


def test_get_mid_video_link():
    """Test case for a valid YouTube link and start time"""
    link = "www.youtube.com/watch?v=dQw4w9WgXcQ"
    start_time = 60  # 1 minute
    expected_result = "youtu.be/dQw4w9WgXcQ?t=60"
    assert get_mid_video_link(link, start_time) == expected_result


@patch("openai.Completion.create")
def test_openai_api_response(mock_completion_create):
    """Mocking the OpenAI API response"""
    # Define a mock response
    mock_response = {"choices": [{"text": "mock response"}]}
    # Set the mock object to return the mock response
    mock_completion_create.return_value = mock_response

    # Call the function that uses the mocked OpenAI API
    # Assuming 'load_data' or any other function interacts with OpenAI
    response = load_data()

    # Assert based on your function's behavior and expected outcomes
    # This is a placeholder assertion, adjust it based on actual use case
    assert response == mock_response
