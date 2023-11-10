# terminal: cd to GoogleCalendar before running

# Issues
# - not able to do reAct
# - bad at using the right functions
# - hallucinate function parameters
import openai
from termcolor import colored
import json
from GoogleCalendar.googleCalendar import *

import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

GPT_MODEL= 'gpt-3.5-turbo'

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

functionNames=["list_calendar_events","create_calendar_event","deleteEvent"]

functions = [
     {
        "name": "deleteEvent",
        "description": "Deletes an event based on the provided eventId.",
        "parameters": {
            "type": "object",
            "properties": {
                "eventId": {
                    "type": "string",
                    "description": "The ID of the event to be deleted."
                }
            },
            "required": ["eventId"]
        }
    },
    {
        "name": "list_calendar_events",
        "description": "Search future events based on query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "query to filter calendar events",
                    }
            },
            "required": [],
        }
    },
    {
        "name": "create_calendar_event",
        "description": "Creates an event on calendar based on given parameters",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the event.",
                },
                "location": {
                    "type": "string",
                    "description": "Location of the event",
                },
                "startDateTime": {
                    "type": "string",
                    "description": "Start date and time of the event in ISO format.",
                },
                "endDateTime": {
                    "type": "string",
                    "description": "End date and time of the event in ISO format.",
                },
                "reminderList": {
                    "type": "array",
                    "description": "List of reminder methods and times.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "method": {
                                "type": "string",
                                "enum": ["email", "popup"]
                            },
                            "minutes": {
                                "type": "integer",
                                "description": "Reminder time in minutes."
                            }
                        }
                    }
                },
                "recurrenceRules": {
                    "type": "string",
                    "description": "Recurrence rule for the event."
                }
            },
            "required": ["title", "location", "startDateTime", "endDateTime"],
        }
    },
]

messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})

def execute_function_call(message):
    print("FUNCTION CALLED: "+ message["function_call"]["name"])
    arguments = json.loads(message["function_call"]["arguments"])
    print("arguments provided:" ) 
    print(arguments)
    if message["function_call"]["name"] == "create_calendar_event":
        results= create_calendar_event(arguments.get("title"),arguments.get("location"),arguments.get("startDateTime"),arguments.get("endDateTime"),arguments.get("reminderList"),arguments.get("recurrenceRules"))
    elif message["function_call"]["name"] == "list_calendar_events":
        results= list_calendar_events(arguments.get("query"))
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    print(results)
    return 

while True:
    output=[]
    #userInput= input("PROMPT: ")
    userInput= "i would like to rock climb next saturday at 1pm. Help me set a reminder 2 days before the event"
    messages.append({"role": "user", "content": userInput})
    chatResponse = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=messages,
        functions= functions
    )
    response= chatResponse["choices"][0]["message"]
    output.append(response)
    messages.append(response)
    if response.get("function_call"):
        results = execute_function_call(response)
        #print(results)
        break
    pretty_print_conversation(output)
