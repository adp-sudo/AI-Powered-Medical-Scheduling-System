from llm import llm
from tools import lookup_patient
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage

#add tools to the llm object

llm_with_tools = llm.bind_tools(
    [lookup_patient]
)

user_input = input("You: ")

#the main prompt

human_message = HumanMessage(
    content=user_input
)

response = llm_with_tools.invoke(
    [human_message]
)

#print(response)
#print(response.tool_calls)



tool_call = response.tool_calls[0]

tool_result = lookup_patient.invoke(
    tool_call["args"]
)



tool_message = ToolMessage(

    content=str(tool_result),

    tool_call_id=tool_call["id"]

)

final_response = llm_with_tools.invoke(
    [
        human_message,
        response,
        tool_message
    ]
)

#print(final_response.content)
print(tool_result)

