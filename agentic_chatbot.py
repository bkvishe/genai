import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI()

def get_weather(city):
    print("🔨 Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    resp = requests.get(url)

    if resp.status_code != 200:
        return "Error in getting weather"
    return f"The weather of {city} is {resp.text}"

def convert_currency(params):
    print("🔨 Tool Called: convert_currency", params)
    try:
        amount, from_currency, to_currency = params.split(",")
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency.strip().upper()}&to={to_currency.strip().upper()}"
        resp = requests.get(url)

        if resp.status_code != 200:
            return "Error in fetching currency conversion"

        data = resp.json()
        converted_value = data["rates"][to_currency.strip().upper()]
        return f"{amount} {from_currency.upper()} = {converted_value} {to_currency.upper()} (as of {data['date']})"
    except Exception as e:
        return f"Invalid input or error: {str(e)}. Use format like: 100, USD, INR"

def run_command(command):
    print("Executing command:", command)
    return os.system(command=command)

system_prompt = """
    You are a helpful assistant who is specialized in solving user queries.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the tool to be used, and then execute the tool.
    Wait for the observation and based on the observation from the tool execution resolve the query.

    Rules:
    - Follow the output json format
    - Always perform one step at a time and wait for the next input
    - Carefully observe the output of the tool and then resolve the query

    Available tools:
    - get_weather: Get the weather of a city
    - convert_currency: Convert currency from one to another. Input should be: <amount>, <from_currency>, <to_currency>

    Output json format:
    {{
        step: "start" | "plan" | "action" | "observe" | "output",
        content: "string" // optional, only for start, plan, observe, output,
        response: "string" // optional, only for observe,
        function: "The name of function if the step is action", 
        input: "The input to the function if the step is action"
    }}

    Example:
    User Query: Convert 100 USD to INR
    Output: {{ "step": "plan", "content": "The user wants to convert 100 USD to INR" }}
    Output: {{ "step": "plan", "content": "I will use the convert_currency tool to get the converted value" }}
    Output: {{ "step": "action", "function": "convert_currency", "input": "100, USD, INR" }}
    Output: {{ "step": "observe", "response": "100 USD = 8340 INR" }}
    Output: {{ "step": "output", "content": "100 USD is equivalent to 8340 INR" }}
"""

messages = [
    {"role": "system", "content": system_prompt},
]

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Get the weather of a city"
    },
    "convert_currency": {
        "fn": convert_currency,
        "description": "Convert currency from one to another"
    }
}

user_query = input("Enter your query: ")
messages.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages,
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

    if parsed_response.get("step") == "plan":
        print(f"🧠Planning: {parsed_response.get('content')}")
        continue

    if parsed_response.get("step") == "action":
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")
        print(f"Executing: {tool_name} with input {tool_input}")

        if available_tools.get(tool_name):
            output = available_tools[tool_name]["fn"](tool_input)
            messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "response": output})})
            continue

    if parsed_response.get("step") == "output":
        print(f"Output: {parsed_response.get('content')}")
        break
