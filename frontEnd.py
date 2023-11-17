import streamlit as st
from streamlit_chat import message
from main import load_calendar_chain
from langchain.memory import ConversationBufferMemory
import datetime
import json 

#init session states
if ("chat_answers_history" not in st.session_state 
    and "user_prompt_history" not in st.session_state 
    and "chat_history" not in st.session_state
    ):
    st.session_state["model_answer_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []
    st.session_state["memory"]= ConversationBufferMemory(memory_key="chat_history", return_messages=True)

st.set_page_config(initial_sidebar_state="collapsed")

## STREAMLIT COMPONENTS
st.title('🦜🔗 Quickstart App')
st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")


#side bar for model settings
with st.sidebar:
    with st.expander("👴 User Information", expanded=False):
        NAME= st.text_input("Name", value="John Doe")
        EMAIL= st.text_input("Email", value="JohnDoe@gmail.com")
        PHONE= st.text_input("Phone", value="91234567")
        LOCATION= st.text_input("Location", value="2299 Piedmont Ave, Berkeley, CA 94720")
        st.session_state["user_info"]= {"name": NAME, "email": EMAIL, "phone": PHONE, "location": LOCATION}
    
    with st.expander("🛠️ Settings ", expanded=False):
        # Option to preview memory store
        MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4','text-davinci-003','text-davinci-002','code-davinci-002'])
        K = st.number_input(' (#)Summary of prompts to consider',min_value=3,max_value=10)

    st.download_button(
        label="Download chat history",
        data= json.dumps(st.session_state["chat_history"]),
        file_name='chat_history_{}.json'.format(datetime.datetime.now()),
        mime='application/json')
    

# initial text input
input_text = st.text_input("Prompt", placeholder="Enter your message here...") or st.button(
    "Submit"
)

#Camera
# picture = st.camera_input("Take a picture") #future expansion?
# if picture:
#     st.image(picture)

#upload audio file
#uploaded_file = st.file_uploader("Choose a file") 

#play audio file
# audio_file = open('/Users/yufei/Desktop/Coding/Academics/CS294-GenAI/media/audio.mp3', 'rb')
# audio_bytes = audio_file.read()
# st.audio(audio_bytes, format='audio/mp3')
         
# def run_llm(input_text):
#    qa= load_chain(MODEL)
#    print(st.session_state["memory"])
#    return qa({"question": input_text,"chat_history": st.session_state["chat_history"] })

def run_Calendar(input_text):
   calendarChain= load_calendar_chain(MODEL,st.session_state["memory"], st.session_state["user_info"])
   response= calendarChain.invoke({"input": input_text})
   generated_response={}
   generated_response["answer"]= response["output"] # for backward compatiability
   return generated_response
    
#act on user's input
if input_text:
   with st.spinner("Generating response..."):
    generated_response=run_Calendar(input_text)
    #generated_response, memory= load_chain(query= input_text, model=MODEL)
    st.session_state.user_prompt_history.append(input_text)
    st.session_state.model_answer_history.append(generated_response["answer"])
    st.session_state.chat_history.append((input_text, generated_response["answer"]))
    st.session_state.memory.save_context({"input": input_text},{"output": generated_response["answer"]})

#populate current conversation
with st.expander("Conversation", expanded=True):
    if st.session_state.model_answer_history:
        for generated_response, user_query in zip(
            st.session_state.model_answer_history,
            st.session_state.user_prompt_history,
        ):
            message(
                user_query,
                is_user=True,
            )
            message(generated_response)