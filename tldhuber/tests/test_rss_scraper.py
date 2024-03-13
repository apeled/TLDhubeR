"""
Unit tests for the RSS Scraper module.

This test suite provides a series of unit tests for the rss_scraper module.
It tests fetching the RSS feed from the Huberman Lab podcast, whether the
columns are named as expected, and tests if expected episode titles are
included in the scrape.
"""

import unittest
import pandas as pd

from tldhuber.utils.rss_scraper import scrape_rss_data


class TestRSSDataScraper(unittest.TestCase):
    """
    Unit tests for the rss_scraper module using the Huberman lab RSS feed.
    """

    def test_scrape_rss_data_smoke_test(self):
        """
        Smoke test of scrape_rss_data function with the Huberman Lab RSS feed URL.
        """
        feed_url = "https://feeds.megaphone.fm/hubermanlab"
        df_result = scrape_rss_data(feed_url)

        # Basic checks to verify the DataFrame structure
        self.assertIsNotNone(df_result)
        self.assertIsInstance(df_result, pd.DataFrame)
        self.assertGreater(len(df_result), 0)

    def test_scrape_rss_data_one_shot_columns(self):
        """
        This function checks for expected columns in the DataFrame.
        """
        feed_url = "https://feeds.megaphone.fm/hubermanlab"
        df_result = scrape_rss_data(feed_url)

        expected_columns = ["Title", "Publication Date", "Summary", "Enclosure Link"]
        for column in expected_columns:
            self.assertIn(column, df_result.columns)

    def test_scrape_rss_data_one_shot(self):
        """
        One-shot test for a specific episode of the Huberman Lab podcast.

        This test verifies that the scraping function can find an episode with a specific title.
        """
        feed_url = "https://feeds.megaphone.fm/hubermanlab"
        df_result = scrape_rss_data(feed_url)

        # Checking for the specific episode by title
        specific_title = (
            "Dr. Mark D'Esposito: How to Optimize Cognitive Function & Brain Health"
        )
        episode_exists = df_result["Title"].str.contains(specific_title).any()
        self.assertTrue(episode_exists)

    def test_scrape_rss_data_invalid_feed(self):
        """
        Test the behavior of scrape_rss_data when given an invalid RSS feed URL or
        if the Huberman feed cannot be parsed.
        
        This edge test verifies that the function returns None when it cannot parse the feed,
        simulating situations where the feed URL is incorrect or the feed is down.
        """
        invalid_feed_url = "https://example.com/invalid_rss_feed"
        result = scrape_rss_data(invalid_feed_url)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
