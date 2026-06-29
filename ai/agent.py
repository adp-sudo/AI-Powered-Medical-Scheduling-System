from llm import llm
from tools import lookup_patient
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage

llm_with_tools = llm.bind_tools(
    [lookup_patient]
)

human_message = HumanMessage(
    content="""
Hi my name is Aayush Deshpande.
I was born on 10/13/2005.
Can you check if I am already registered?
"""
)

response = llm_with_tools.invoke(
    [human_message]
)

#print(response.tool_calls)

tool_call = response.tool_calls[0]

tool_result = lookup_patient.invoke(
    tool_call["args"]
)

#print(tool_result)

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

print(final_response.content)