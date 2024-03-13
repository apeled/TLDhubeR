# TLDHubeR---A Search Tool for the Andrew Huberman Podcast
[![build_test](https://github.com/apeled/TLDhubeR/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/apeled/TLDhubeR/actions/workflows/python-package-conda.yml)
[![Coverage Status](https://coveralls.io/repos/github/apeled/TLDhubeR/badge.svg?branch=main)](https://coveralls.io/github/apeled/TLDhubeR?branch=main)

## Project Overview

Andrew Huberman is a double threat---a neuroscientist by day and a podcast host by night. He's a professor at Stanford University digging into the hows and whys of our brains, and his Huberman Lab Podcast is wildly popular, reaching #1 on health and fitness on major platforms.

Our application, TLDHubeR,  allows users to search for and summarize content in the Huberman Lab Podcast using a chat interface, all from the comfort of their browser. Ask a question, any question, and the app will search the Huberman Lab for relevant information and then use that information to generate a response, including relevant youtube links. Whether you're new to the podcast or a longtime fan, we hope TLDHubeR will help you parse the many hours of the Huberman Lab for learning and pleasure!

### Team 

Below is team that worked on this application. If you have any questions, feel free to reach out to us on github!

| Name | Github Handle | 
|---|---|
| Edouard Seryozhenkov| edouas  | 
| Mark Daniel | MarkUnivWash | 
| Amit Peled | apeled | 
| Jake Flynn | jakeflynn56 | 


### Project Goals

This project is a search and summary ***tool*** written in Python. Our team aimed to create an application that would be convenient, educational, and fun for a general audience. In order to accomplish this goal, we implemented functionality so that our users to be able to input a question or search term, and receive in turn:

- A search response that summarizes relevant content from the Huberman Lab and quotes the podcast.
- An embedded YouTube video that allows users to start listening to the podcast right when relevant discussions begin.
  - Additional relevant links with timestamps, for follow up exploration.

We also want to guide our users through this process, especially if they are unfamiliar with the Huberman Lab. We include side page for this reason, and also gently prompt users who would rather not take the time to peruse it.

### Setup Guide

[To set up TLDHubeR and run it locally, click this link and follow our guide! See the tree structure at the bottom of this README for how the installation should look.](examples/README.md)

[If you want to see TLDHubeR in action, click this link for a short video demo!](https://drive.google.com/file/d/1fiSpdIgGcz334ju89eA-xbq1F2fx2haV/view?usp=sharing)

## Data Sources & Additional Info

Our application uses data from two sources to generate the database that we use in our app. These include:
- The RSS feed of the Huberman Lab (metadata).
- Andrew Huberman's YouTube channel (video links, id's, and podcast transcripts).

These data sources were scraped and the output was then joined into a single podcasts dataset. Until we configure hosting, we are termporarily storing this data [here](https://drive.google.com/drive/folders/1-DpJ9uRG-6wK9yiYZPyIj181-QSbK0_l?usp=sharing).

### Overall Project Structure After Setup

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
