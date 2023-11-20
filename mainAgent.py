from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from pydantic.v1 import BaseModel, Field
from langchain.callbacks import HumanApprovalCallbackHandler
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.chains import LLMChain
from langchain.schema.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from googleCalendar import *
from calendarAgent import *
from typing import Dict
from datetime import date
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool
from infoRetriever import *
import os
from dotenv import load_dotenv
load_dotenv()

from emailFunc import *

OPENAI_API= os.getenv('OPENAI_API_KEY')
SERPAPI_API_KEY= os.getenv('SERPAPI_API_KEY')

search = SerpAPIWrapper()
class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")

tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
            args_schema=SearchInput
        ),
    ]
#unable to create agents like the above method as agents take in a specified input of {"input"=userInput}

prompt_template_string= "You are a helpful assistant. You manage calender events, doordash orders, maps navigation and report on the news.  Clarify function arguments if needed. You also have access to the records of when he has taking his medication, by accessing files which are stored in the data folder. Do not assume the file's name, list the files to identify file of interest. Today's date is {currentDate}. Here are the user's particulars, use it if needed. You are currently chatting with {name}, his address is {address}, his/her email is {email}, and his/her phone number is {phone}."


def load_main_agent(model, memory, user_info):
    """Loads the tools"""
    def calendar_agent(userInput:str)-> str:
        """Useful to perform calendar related tasks (create, delete, list events)"""
        agent= load_calendar_chain_no_memory("gpt-3.5-turbo", user_info)
        return agent.invoke({"input": userInput})

    def doordash_agent(userInput:str)-> str:
        """Useful to perform doordash related tasks (create order or check on order status)"""
        agent= load_calendar_chain_no_memory("gpt-3.5-turbo", user_info)
        return agent.invoke({"input": userInput})

    def maps_agent(userInput:str)-> str:
        """Useful to perform google maps related tasks"""
        agent= load_calendar_chain_no_memory("gpt-3.5-turbo", user_info)
        return agent.invoke({"input": userInput})

    def news_agent(userInput:str)-> str:
        """Useful to perform news related tasks"""
        agent= load_calendar_chain_no_memory("gpt-3.5-turbo", user_info)
        return agent.invoke({"input": userInput})

    tools.append(StructuredTool.from_function(calendar_agent))
    # tools.append(StructuredTool.from_function(doordash_agent))
    # tools.append(StructuredTool.from_function(maps_agent))
    # tools.append(StructuredTool.from_function(news_agent))
    tools.append(StructuredTool.from_function(list_files, name="list medical records", description="list files in the data folder"))
    tools.append(StructuredTool.from_function(read_file, name= "read medical records", description="read a record of the days medication wasin the data folder"))
    tools.append(StructuredTool.from_function(send_email, name= "send email", description="sends an email to an intended recipient"))
    

    """Loads the main agent"""
    llm = ChatOpenAI(temperature=0, model=model)
    prompt_string=prompt_template_string.format(currentDate=date.today().strftime("%B %d, %Y"), name= user_info["name"], address= user_info["location"], email= user_info["email"],phone= user_info["phone"])
    memory= ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    chat_history=MessagesPlaceholder(variable_name="chat_history")
    agent=initialize_agent(tools=tools,llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs={'prefix': prompt_string,"input_variables": ["chat_history"],"memory_prompts": [chat_history],}, memory= memory)
    return agent


if __name__ == "__main__":
    user_info={}
    user_info["name"]="John Doe"
    user_info["email"]="JohnDoe@gmail.com"
    user_info["phone"]="91234567"
    user_info["location"]="2299 Piedmont Ave, Berkeley, CA 94720"

    prompt_string=prompt_template_string.format(currentDate=date.today().strftime("%B %d, %Y"), name= user_info["name"], address= user_info["location"], email= user_info["email"],phone= user_info["phone"])

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    
    memory= ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    chat_history=MessagesPlaceholder(variable_name="chat_history")

    agent=initialize_agent(tools=tools,llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs={'prefix': prompt_string,"input_variables": ["chat_history"],"memory_prompts": [chat_history],}, memory= memory)

    #response= agent.run("create a calendar event for tea time at 10am tomorrow for 30 minutes at Strate Cafe")
    #response= agent.run("retrieve the dates from the records file for which I took my diabetes medication")
    response= agent.run("send an email to joshua wishing him a happy birthday")

    print(response)