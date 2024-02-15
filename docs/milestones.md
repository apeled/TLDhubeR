# List of Milestones

Milestones. A preliminary plan - a list of milestones, each with a list of tasks in priority order.

### Core:

1. Join our data sources into a single json file. 
   + Include as attributes:
     + Title
     + Guest
     + Summary
     + Timestamps
     + Keywords (may need to use LLM to generate, or LlamaIndex)
   + Process:
     + Transcript -> subsections, based on timestamps from RSS feed
     + Add start time to chunks
     + Include metadata of parent document in each subsections. 

2. Create a data loading pipeline that will parse the podcasts as documents and each subsection
as nodes. It should also attach the correct metadata in the JSON to each chunk. 

3. Implement keyword-based search for best match chunks based on content
   + Configure prompt plus a `Pydantic Program` to return title + youtube links + document id from the returned chunks (top k results) into a data structure.

4. Display the response and embed the videos in the app.
   + Configure our UI to work with multiple search results

### Extras:

5. Implement keyword-based search for a best match podcast (podcast recommendation)
   + If necessary, create an alternative Index and prompt optimized for searching for matches to podcast summaries.
   + Implement a means to route the query to this alternative index (a drop down "mode" selector, or a LlamaIndex `RouterQueryEngine`).

6. Implement podcast summary, given podcast title
   + If necessary, create an alternative Index and prompt optimized for summarizing the documents .
   + Include this mode in the mode selector.

7. Implement a button to fetch more results using the LlamaIndex `refine` response mode.

8. Implement text-to-voice so that search results or summaries can be listened to.
