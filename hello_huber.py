import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

st.set_page_config(page_title="TLDHubeR", page_icon="🧠", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("TLDHubeR---Search and Summarize the Huberman Lab")
st.info("Hint: Are you a Hube noob? If so, try searching for sleep!")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Andrew Huberman's Recent Podcast with David Goggins"}
    ]


def load_data():
    with st.spinner(text="Loading and indexing the Huberman Lab Podcast!"):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-0125-preview", temperature=0.5, system_prompt="In your context is a an episode of the Huberman Lab with metadata including a title, a summary, a youtube link, some timestamps of when certain topics were discussed, and a transcript. Assume all questions are about this podcast, and provide concicse answers that begin as follows: 'RESULTS: ' and quote the text in your context."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Search Query"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history

            
# Clear session state function
def clear_session_state():
    for key in st.session_state.keys():
        st.session_state[key] = None