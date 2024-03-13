#!/usr/bin/env python
# coding: utf-8

"""
This module provides functionality to scrape data from RSS feeds and return it
as a pandas DataFrame. It relies on the feedparser and pandas libraries to parse
the feed and manage the data, respectively.

Author: Jake Flynn
Date: 2024-02-20
"""
#pylint: disable=E0401
import feedparser
import pandas as pd

def scrape_rss_data(feed_url):
    """
    Scrape RSS feed data and return a pandas DataFrame.

    Parameters:
    feed_url (str): The URL of the RSS feed to scrape.

    Returns:
    pandas.DataFrame: A DataFrame containing the scraped RSS feed data,
                      or None if the feed could not be parsed.
    """
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    # Check if the feed was parsed successfully
    if feed.bozo == 0:
        data = []
        # Extract relevant data from each entry
        for entry in feed.entries:
            summary = entry.get('summary', '')
            pubdate = entry.get('published', '')
            title = entry.get('title', '')
            enclosure_link = entry.enclosures[0]['href'] if entry.get('enclosures') else None
            data.append({
                'Title': title,
                'Publication Date': pubdate,
                'Summary': summary,
                'Enclosure Link': enclosure_link
            })
        return pd.DataFrame(data)

    print(f"Error parsing feed: {feed.bozo_exception}")
    return None
