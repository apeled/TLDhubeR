# TLDHubeR---A Search Tool for the Andrew Huberman Podcast


## Project Overview

TLDHubeR is a web application that allows users to search for and summarize content in the Andrew Huberman podcast.

### Project Type

This project is a search and summary ***tool*** written in Python. This project also includes a dataset generation phase, which we are working through using cloud services.

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
