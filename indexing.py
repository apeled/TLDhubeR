from llama_index import Document, VectorStoreIndex, get_response_synthesizer
# from llama_index.schema import TextNode, NodeRelationship, RelatedNodeInfo
# from llama_index.node_parser import SentenceSplitter
# from llama_index.extractors import (
#     SummaryExtractor,
#     QuestionsAnsweredExtractor,
#     KeywordExtractor,
#     EntityExtractor,
# )
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
import json
import os
import nest_asyncio


def load_json_transcripts(base_path):
    """
    Get all filenames with json extensions in the folder at base path. For now we just
    have json, but we may include some .txt files in the future

    Args:
    - base_path (str): Path to the data folder.

    Returns:
    - podcasts_as_json: List of podcast transcripts as json
    """
    podcasts_as_json = []
    for filename in os.listdir(base_path):
        if filename.endswith(".json"):
            path = base_path + "/" + filename
            with open(path, "r") as file:
                podcasts_as_json.append(json.load(file))

    return podcasts_as_json


def parse_into_documents(podcast_jsons):
    """Parses the jsons into a list of Document objects

    Args:
        json: a json file containing a podcast transcript with metadata

    Returns:
        document_list: A list of Document objects corresponding to document subsections
    """
    documents = []
    for pc_json in podcast_jsons:
        podcast_metadata = {
            "episode_title": pc_json["title"],
            "episode_number": pc_json["ep_num"],
            # "episode_summary" : pc_json["episode_summary"],
            "youtube_link": pc_json["link"],
        }
        chunk_list = [chunk for chunk in pc_json["chunks"]]
        for chunk in chunk_list:
            chunk_metadata = podcast_metadata.copy()
            chunk_metadata["timestamp"] = chunk["timestamp"]
            chunk_text = chunk["text"]
            document = Document(text=chunk_text, metadata=chunk_metadata)
            documents.append(document)
    return documents


def get_simple_hube_engine(documents):
    """Makes a simple query engine that uses only the embeddings. Returns
    the context that would be fetched for the LLM, up to 20 nodes.

    Args:
        documents: A list of Document objects corresponding to podcast subsections

    Returns:
        simple_hube_engine: A query engine in "no_text" response mode
    """
    # Build a simple index from the documents
    index = VectorStoreIndex.from_documents(documents)

    # Configure a retriever using this index
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=20,
    )

    # Configure response synthesizer
    response_synthesizer = get_response_synthesizer(response_mode="no_text")

    # Assemble the query engine
    simple_hube_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )

    return simple_hube_engine


def get_mid_video_link(link, t):
    """Transforms a base youtube url to link to time t (seconds) in that video"""
    base_url = link.replace("www.youtube.com/watch?v=", "youtu.be/")
    return base_url + "?t=" + str(t)


def extract_metadata(response):
    """Extracts metadata from the source nodes of a query engine response.

    Args:
        response: The query engine response containing the best match nodes

    Returns:
        metadata_list: a list of containing the metadata of the retrieved nodes
    """
    metadata_list = [node.metadata for node in response.source_nodes]
    for metadata in metadata_list:
        base_link = metadata["youtube_link"]
        start_time = metadata["timestamp"]
        metadata["youtube_link"] = get_mid_video_link(base_link, start_time)
    return metadata_list


if __name__ == "__main__":
    # Sample usage of the functions
    podcast_jsons = load_json_transcripts("./test_data") # Put a few test podcasts in a test ./data folder
    documents = parse_into_documents(podcast_jsons)
    query_engine = get_simple_hube_engine(documents)
    response = query_engine.query("motivation")
    print(extract_metadata(response))
