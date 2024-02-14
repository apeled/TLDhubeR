# List of Milestones

Milestones. A preliminary plan - a list of milestones, each with a list of tasks in priority order.

1. Join our data sources into a single json file. 
   + Include as keys:
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

3. Implement keyword-based search for best match podcasts based on content
   + Load data into a keyword table index? Not 100% sure what this does
   + Configure prompt plus "Pydantic" object to return title + youtube links + document id

4. Implement keyword-based search within a podcast
   + Select the document in the index by document id
   + Configure prompt plus "Pydantic" object to return timestamps + youtube links + tldr summaries

5. Implement cross podcast keyword-based search

