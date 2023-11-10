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
from GoogleCalendar.googleCalendar import *
from datetime import date

import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API= os.getenv('OPENAI_API_KEY')
SERPAPI_API_KEY= os.getenv('SERPAPI_API_KEY')

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")

class DeleteCalendarEventInput(BaseModel):
    event: str = Field(description="Calendar event id of event to delete")

from langchain.tools import StructuredTool #tools from functions
createEventTool= StructuredTool.from_function(create_calendar_event)
listEventTool= StructuredTool.from_function(list_calendar_events)
deleteEventTool= StructuredTool.from_function(deleteEvent)
currentDateTimeTool= StructuredTool.from_function(currentDateTime)

#createEventTool.callbacks= [HumanApprovalCallbackHandler()] #human approval requirememt

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
        args_schema=SearchInput
    ),
]
tools.append(createEventTool)
tools.append(deleteEventTool)
tools.append(listEventTool)
tools.append(currentDateTimeTool)

today = date.today()

prefix="""
    You are a helpful assistant that manages Tom's calendar events. 
    Do not assume the current date or any of the function's arguments.
    Today's date is {}.
""".format(today.strftime("%B %d, %Y"))
print(prefix)

from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
chat_history = MessagesPlaceholder(variable_name="chat_history")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent= initialize_agent(tools, llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs={'prefix': prefix, "memory_prompts": [chat_history]}, memory= memory)


if __name__ == "__main__":
    #sanity check for memory
    # print(agent.run("my name is bob"))
    # print(agent.run("what is my name"))
    userInput= input("Chat with me!\n")
    intermediateSteps=[]
    while True:
        output= agent.invoke({"input": userInput})
        print(memory)
        print(output["output"])
        #print(output) #keys: input, chat_history, output
        userInput=input()


def load_calendar_chain(model,chatMemory):
    chat_history=MessagesPlaceholder(variable_name="chat_history")
    agent= initialize_agent(tools,llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs={'prefix': prefix,"memory_prompts":[chat_history]}, memory= chatMemory)
    return agent