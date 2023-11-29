# ElderGPT | CS294 Responsible GenAI and Decentralized Intelligence

## Background
Despite high mobile phone ownership among the elderly, many struggle to utilise various mobile applications due to their complex and varied nature. We hope to tackle this issue through ElderGPT, a one-stop elderly-friendly gateway to interact with various mobile applications

## Core Functionality

### Text and Speech Interaction
- Ability to converse with the model using speech. Supports different languages (using Streamlit)
- Ability to read out model output using different agents and varying speaking rates (using ElevenLabs API)
### Integration with various applications
- Langchain agent is equipped with custom tools for Google Calendar, Google Translate, Google Maps, News, Door Dash, email

## Product Demonstration
[![Product Demonstration](https://img.youtube.com/vi/TCu4E8D3HCI/0.jpg)](https://www.youtube.com/watch?v=TCu4E8D3HCI)
## Running Locally
1. Clone the repository
```sh
git clone https://github.com/Ranchu2000/ElderGPT.git
```
2. Set up .env file (refer to env_template.txt)

3. Enter the directory
```sh
cd ElderGPT
```
4. Install the dependencies
```sh
pip install requirements.txt
```
5. Run the app
```sh
streamlit run ./frontEnd.py
```

## Developers
- [Jacky Kwok](https://github.com/jackyk02)
- [Jianan Cai](https://github.com/Jianan-Jackson)
- [Shubhangam Prasad](https://github.com/ShubhangamPrasad)
- [Wong Yu Fei](https://github.com/Ranchu2000)