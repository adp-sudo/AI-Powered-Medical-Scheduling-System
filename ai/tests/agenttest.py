from llm import llm
from tools import lookup_patient

from langchain_core.messages import HumanMessage, ToolMessage

# Give the LLM access to our tools
llm_with_tools = llm.bind_tools([lookup_patient])

# Get input from the user
user_input = input("You: ")

# Convert the input into a HumanMessage
human_message = HumanMessage(content=user_input)

# Send the message to the LLM
response = llm_with_tools.invoke([human_message])

# Print what the LLM decided to do
print(response)
print(response.tool_calls)

# If no tool was needed, print the response and stop
if not response.tool_calls:
    print(response.content)
    exit()

# Get the tool the LLM wants to call
tool_call = response.tool_calls[0]

# Execute the tool using the arguments chosen by the LLM
tool_result = lookup_patient.invoke(tool_call["args"])

# See what the tool returned
print(tool_result)

# Convert the tool output into a ToolMessage
tool_message = ToolMessage(
    content=str(tool_result),
    tool_call_id=tool_call["id"]
)

# Send the original message, tool request, and tool result
# back to the LLM so it can generate the final answer
final_response = llm_with_tools.invoke(
    [
        human_message,
        response,
        tool_message
    ]
)

# Print the final answer
print(final_response.content)