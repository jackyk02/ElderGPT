import streamlit as st
from streamlit_chat import message
from model import load_chain

#init session states
if ("chat_answers_history" not in st.session_state 
    and "user_prompt_history" not in st.session_state 
    and "chat_history" not in st.session_state
    ):
    st.session_state["model_answer_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

## STREAMLIT COMPONENTS
# header
st.title('🦜🔗 Quickstart App')
st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")
#side bar for model settings
with st.sidebar.expander("🛠️ ", expanded=False):
    # Option to preview memory store
    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4','text-davinci-003','text-davinci-002','code-davinci-002'])
    K = st.number_input(' (#)Summary of prompts to consider',min_value=3,max_value=1000)

# initial text input
input_text = st.text_input("Prompt", placeholder="Enter your message here...") or st.button(
    "Submit"
)
def run_llm(input_text):
   qa= load_chain(MODEL)
   return qa({"question": input_text,"chat_history": st.session_state["chat_history"] })
    
#act on user's input
if input_text:
   with st.spinner("Generating response..."):
    generated_response=run_llm(input_text)
    #generated_response, memory= load_chain(query= input_text, model=MODEL)
    st.session_state.user_prompt_history.append(input_text)
    st.session_state.model_answer_history.append(generated_response["answer"])
    st.session_state.chat_history.append((input_text, generated_response["answer"]))

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