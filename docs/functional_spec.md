# Background

A typical episode of the Huberman Lab podcast ranges from 1 to 4 hours in duration. During those hours, many topics, ideas, studies, events, and people may be discussed. Even for an avid listener, it is nearly impossible to keep track of the volume of content contained in a typical episode. Podcasts are not designed for efficient knowledge transfer or to be consistent references, and the Huberman Lab is no exception. Still, there is a wealth of information that many would love to extract, retrieve, remember, or learn.

Our project aims to solve this problem by deploying a GPT-powered web app that will allow users to search and summarize the Huberman Lab podcast. In doing so, we aim to aid listener recall and allow users who are interested in the informational content of the Huberman Lab a more efficient way to get the big picture.

# Data Source

The data source we are leveraging for this project is a dataset of podcast transcripts and metadata that we have compiled ourselves from the RSS feed of the Huberman Lab and by using the YouTube Transcript API and Youtube Data API. We have stored the podcasts in JSON and have chunked the transcript based on the podcast sections provided in the feed.

## User Stories and Use Cases

### General User Profile

In general, we expect our users to be individuals who value simple, intuitive interfaces and who are interacting with our app to satisfy curiosity or save time. We expect them all to be familiar with services such as Google and YouTube and able to use similar interfaces without having to learn them. In short, we expect them to be casual, non-technical users who are using the app in a personal and not professional context.

### User 1:

Alice is a longtime fan of the Huberman Lab. She remembers a certain topic being discussed on the podcast but doesn't remember what was said or where exactly the topic was discussed. Alice wants to find out in which episodes her topic of interest was discussed and when. Alice is accustomed to using search engines like Google and values a simple interface. Unfortunately, Google search results are just not specific enough for her needs.

#### Use Cases

1. Alice wants to input a keyword or keywords into a webpage chat box. She expects to see a display containing a short list of Huberman Lab podcasts in which those keywords were discussed.
2. Alice wants to be able to click a button to get more search results if they exist. She expects for the website to add more items to the list.
3. Alice wants to see timestamps of when the topic was discussed in the podcast, so she knows exactly when to start watching. 
   + She expects to receive a timestamp at the least, but Alice would prefer a YouTube video of the podcast to pop up that begins at the timestamp.

### User Story 2:

Bob has never listened to an episode of the Huberman Lab. His friend is recommending he check out a particular episode. The problem is, Bob doesn't want to spend 3 hours listening to a podcast (it's not his thing). Bob wants to input the title of the episode and get a summary of it in return. Bob doesn't know the exact title of the podcast, so he needs a tool that can work with approximate input. Bob also values a simple, intuitive interface that he will not have to learn. 

#### Use Cases
1. Bob wants to input the approximate title of a podcast and expects to see a display containing a summary of that podcast that concisely lists main points and recommendations.
2. Bob wants to be able to interact with the summarizer by asking it in natural language to elaborate on its summary in various ways. He expects a response the display to continue a conversation with him about the summary without hallucinating or going off-topic.
3. Bob wants to see which sources were cited within the podcast, as well as the names of guests (if any) that appear on the podcast. He expects to see a list of these results.

### User Story 3:

Mark has listened to a fair amount of the Huberman Lab, and if there's one thing he knows, it's that Andrew loves to talk about dopamine. But what is the gist of it all? Mark wants to input the word "dopamine" and get a summary of the discussion of the topic *across all episodes of the Huberman Lab*. Mark is like Alice and Bob in that he values a simple, Google-like interface.

#### Use Cases
1. Mark wants to input search terms and he expects to see a display containing a summary of the content pertaining to those terms across all the podcasts in the dataset. 
2. Mark, like Alice, wants to be able to press a button to have the model elaborate on its summary. He expects the model to do so quickly and with no hallucinations.
