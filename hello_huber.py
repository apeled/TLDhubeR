import streamlit as st
import openai
from llama_index import VectorStoreIndex,SimpleDirectoryReader,ServiceContext
from llama_index.llms import OpenAI
import re

st.set_page_config(page_title="TLDHubeR", page_icon="🧠", layout="centered", initial_sidebar_state="auto", menu_items=None)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/apeled/TLDhubeR)"

markdown_file_path = 'docs/tldhuber_side_page.md'

# Reading the content of the markdown file
with open(markdown_file_path, 'r', encoding='utf-8') as file:
    markdown_content = file.read()

# Displaying the content in the sidebar
st.sidebar.markdown(markdown_content, unsafe_allow_html=True)

openai.api_key = openai_api_key
st.title("TLDHubeR---Search and Summarize the Huberman Lab")
st.info("Hint: Are you a Hubernoob? If so, try searching for sleep!")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about my Recent Podcast with David Goggins"}
    ]

def load_data():
    with st.spinner(text="Loading and indexing the Huberman Lab Podcast!"):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-0125-preview",temperature=0.5, system_prompt="In your context is a an episode of the Huberman Lab with metadata including a title, a summary, a youtube link, some timestamps of when certain topics were discussed, and a transcript. Assume ALL questions I ask are about THIS podcast, and provide concise answers that begin as follows: 'RESULTS: ' and quote the text in your context. 'TIMESTAMP: 'and give the timestamp in your context. List the time stamps in brackets separated by commas. 'YOUTUBE LINK: ' ALWAYS provide the 'link' in your context."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

try:
    index = load_data()
    if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    if prompt := st.chat_input("Search Query"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for i,message in enumerate(st.session_state.messages): # Display the prior chat messages
        # with st.chat_message('assistant' ,avatar="./docs/andrew.jpeg"):
        if i == 0:
            with st.chat_message(message["role"],avatar="./docs/andrew.jpeg"):
                st.write(message["content"])

        else:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="./docs/andrew.jpeg"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) # Add response to message history

                part_index = message['content'].find("YOUTUBE LINK: ")
                numbers_match_single = re.findall(r"TIMESTAMP: \[([0-9, ]+)\]", message['content'])
                result = None
                
                if numbers_match_single:
                    numbers_list_single = [int(num.strip()) for num in numbers_match_single[0].split(',')][0]
                else:
                    numbers_list_single = 0  # No timestamp matches found

                if part_index != -1:
                    result = message['content'][part_index + len("YOUTUBE LINK: "):]
                if result and ".com" in result:
                    st.video('result', start_time=numbers_list_single)
                
                col1, col2 = st.columns(2)
                with col1:
                    with st.expander("See addtional time stamps"):
                        st.write("[Insert time stamps]")
                with col2:
                    with st.expander("See additional podcasts"):
                        st.write("[Insert additional podcast links]")
except:
    if openai.api_key:
        st.error("The OpenAPI key entered is invalid. Please enter a valid OpenAPI key.")
    else:
        st.warning("Enter your OpenAPI key in the sidebar")
            
# Clear session state function
def clear_session_state():
    for key in st.session_state.keys():
        st.session_state[key] = None
