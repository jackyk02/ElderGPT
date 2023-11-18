import streamlit as st
from st_audiorec import st_audiorec
## STREAMLIT COMPONENTS
st.title('🦜🔗 Quickstart App')
st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")

#init session states
st.subheader("Record audio")
wav_audio_data = st_audiorec()

#Camera
# picture = st.camera_input("Take a picture") #future expansion?
# if picture:
#     st.image(picture)

#upload audio file
#uploaded_file = st.file_uploader("Choose a file") 
st.subheader("Play audio file")

#play audio file
audio_file = open('/Users/yufei/Desktop/Coding/Academics/CS294-GenAI/media/audio.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')
  
input_text = st.text_input("Prompt", placeholder="Enter your message here...", key="userPrompt")