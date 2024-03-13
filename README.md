# TLDHubeR---A Search Tool for the Andrew Huberman Podcast

## Project Overview

TLDHubeR is a web application that allows users to search for and summarize content in the Huberman Lab Podcast using a chat interface. Essentially it is retrieval augmented generation app with extra quality of life features powered by `llama-index` and `streamlit`. 

### Project Type

This project is a search and summary ***tool*** written in Python. 

### Questions of Interest

We want our users to be able to input a search string or search term, and receive in turn:
- A podcast that is the "closest match" in content to the search terms
- Timestamps of when those terms are discussed in the match
- An embedded YouTube video that allows users to start listening right when those discussions begin
- A short summary of the contents of the search results, including the relevant transcript, with any sources the podcast may have cited

### Goal for the Project Output

The primary output of this project will be a web application with an LLM (gpt-4-turbo) hiding in the backend, configured to act as a search engine with retrieval augmented generation (RAG). A necessary preliminary goal on the way to this is to compile a high quality and up to date dataset for the Andrew Huberman podcast, including episode transcripts, which we plan to share online.

In accomplishing these two goals we hope to enable users to filter the podcast based on their interests, to quickly find content they have heard before, and to get their hands on the data if they'd like.

### Data Sources
As of now, we plan to use three sources of data in our application:
- Podcast metadata scraped from Andrew Huberman's RSS feed (done).
- Podcast transcripts which we are generating using audio transcription models (in progress).
- Data from Andrew Huberman's YouTube channel (in progress).

### Overall Project Structure

```{bash}
.
├── LICENSE
├── README.md
├── data
│   ├── default__vector_store.json
│   ├── docstore.json
│   ├── graph_store.json
│   ├── image__vector_store.json
│   └── index_store.json
├── docs
│   ├── DATA 515 Tech Review.pdf
│   ├── andrew.jpeg
│   ├── component_spec.md
│   ├── functional_spec.md
│   ├── milestones.md
│   ├── sequence_diagram.png
│   ├── sequence_diagram.txt
│   └── tldhuber_side_page.md
├── environment.yml
├── examples
│   ├── README.md
│   └── site_navigation.md
├── notebooks
│   ├── indexing.ipynb
│   ├── mergeRSSandTranscripts.ipynb
│   ├── rss_scraper.ipynb
│   └── scrapeTranscripts.ipynb
├── pyproject.toml
├── scraped_data
│   ├── RAW_UU2D2CMWXMOVWx7giW1n3LIg_youtube_videos.json
│   └── rss.csv
└── tldhuber
    ├── __init__.py
    ├── hello_huber.py
    ├── static
    │   ├── api_key.png
    │   ├── chat_example.png
    │   ├── chat_interface.png
    │   ├── download.jpeg
    │   └── load_index.png
    ├── tests
    │   ├── __init__.py
    │   ├── test_data
    │   │   ├── test.json
    │   │   ├── test_nodes.pkl
    │   │   └── test_output
    │   │       └── test_output.pkl
    │   ├── test_hello_huber.py
    │   ├── test_indexing.py
    │   ├── test_rss_scraper.py
    │   └── test_transcripts_scraper.py
    |
    └── utils
        ├── indexing.py
        ├── merge_rss_and_transcripts.py
        ├── rss_scraper.py
        └── transcripts_scraper.py
```