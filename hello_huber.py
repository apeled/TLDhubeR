"""
Module for setting up a Streamlit application that searches and summarizes content
from the Huberman Lab Podcast. Uses llama_index for data indexing and retrieval, and
OpenAI for text embedding and generation.
"""

import streamlit as st
import openai

from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    get_response_synthesizer,
    Settings
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Configuration of the Streamlit page
st.set_page_config(
    page_title="TLDHubeR",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Markdown file path
MARKDOWN_FILE_PATH = 'docs/tldhuber_side_page.md'

def read_markdown_file(path):
    """
    Reads the content of a markdown file and returns it.
    
    Parameters:
        path (str): The path to the markdown file.
        
    Returns:
        str: The content of the markdown file.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

# Displaying the content in the sidebar
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View the source code](https://github.com/apeled/TLDhubeR)")
    st.markdown(read_markdown_file(MARKDOWN_FILE_PATH), unsafe_allow_html=True)

openai.api_key = openai_api_key
st.title("TLDHubeR: Search and Summarize the Huberman Lab")
st.info("Hint: Are you a Hubernoob? If so, try searching for sleep!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Ask me a question about my podcasts."}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    """
    Loads and indexes the Huberman Lab Podcast data, initializing settings for keyword
    extraction and text embedding.
    
    Returns:
        VectorStoreIndex: The loaded and indexed podcast data.
    """
    with st.spinner("Loading and indexing the Huberman Lab Podcast!"):
        Settings.llm = OpenAI(temperature=0.2, model="gpt-3.5-turbo-0125")
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

        storage_context_load = StorageContext.from_defaults(persist_dir="./data")
        loaded_index = load_index_from_storage(storage_context_load)

        return loaded_index

def set_up_engine(loaded_index):
    """
    Creates a retriever and query engine using the loaded index.
    
    Parameters:
        loaded_index (VectorStoreIndex): The loaded and indexed podcast data.
        
    Returns:
        RetrieverQueryEngine: The assembled query engine.
    """
    retriever = VectorIndexRetriever(index=loaded_index, similarity_top_k=10)
    response_synthesizer = get_response_synthesizer(response_mode="no_text")

    simple_hube_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.25)]
    )
    return simple_hube_engine

def get_mid_video_link(link, t):
    """
    Modifies a YouTube link to start at a specified time.
    
    Parameters:
        link (str): The original YouTube video link.
        t (int): The start time in seconds.
        
    Returns:
        str: The modified YouTube link with the start time parameter.
    """
    base_url = link.replace("www.youtube.com/watch?v=", "youtu.be/")
    return f"{base_url}?t={t}"

def extract_metadata(query_response):
    """
    Extracts and transforms metadata from source nodes in a query response.
    
    Parameters:
        query_response (QueryResponse): The response from a query engine.
        
    Returns:
        list[dict]: A list of transformed metadata dictionaries with modified YouTube links.
    """
    metadata_list = [node.metadata for node in query_response.source_nodes]
    for metadata in metadata_list:
        base_link = metadata["youtube_link"]
        start_time = metadata["timestamp"]
        metadata["youtube_link"] = get_mid_video_link(base_link, start_time)
    return metadata_list

# Main application logic
try:
    if openai.api_key:
        index = load_data()
        engine = set_up_engine(index)
        if "chat_engine" not in st.session_state:
            st.session_state["chat_engine"] = index.as_chat_engine(
                chat_mode="context",
                system_prompt="""Respond as if you are Andrew Huberman. You should answer by
                                summarizing the topic from your context. Always
                                include a direct quote from your podcast related to
                                the response."""
            )

        if prompt := st.chat_input("Search Query"):
            st.session_state["messages"].append({"role": "user", "content": prompt})
            vector_response = engine.query(prompt)
            meta_data = extract_metadata(vector_response)
            youtube_links = [episode['youtube_link'] for episode in meta_data]
            timestamps = [episode['timestamp'] for episode in meta_data]

        for i, message in enumerate(st.session_state["messages"]):
            with st.chat_message(message["role"], avatar="./docs/andrew.jpeg" if i == 0 else None):
                st.write(message["content"])

        if st.session_state["messages"][-1]["role"] != "assistant":
            with st.chat_message("assistant", avatar="./docs/andrew.jpeg"):
                with st.spinner("Thinking..."):
                    response = st.session_state["chat_engine"].chat(prompt)
                    st.write(response.response)
                    message = {"role": "assistant", "content": response.response}
                    st.session_state["messages"].append(message)
                    st.video(youtube_links[0], start_time=timestamps[0])

                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander("See additional time stamps"):
                            for timestamp in timestamps[1:]:
                                st.write(f"{timestamp} seconds")
                    with col2:
                        with st.expander("See additional podcasts"):
                            for episode in youtube_links[1:]:
                                st.write(episode)
except Exception as e:
    if openai.api_key:
        st.error(f"An error occurred: {e}. Please check your OpenAPI key and try again.")
    else:
        st.warning("Enter your OpenAPI key in the sidebar.")

def clear_session_state():
    """
    Clears the Streamlit session state.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
