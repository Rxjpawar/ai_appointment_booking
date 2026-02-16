from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.constants import START
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from app.mem_config import mem_client
from app.prompt import prompt
from app.database.tools import book_appointment,list_appointments,cancel_appointment,get_current_date_time
load_dotenv()

# llm = init_chat_model(model_provider="openai", model="gpt-4o-mini")
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")
available_tools = [get_current_date_time,book_appointment,list_appointments,cancel_appointment]

llm_with_tools = llm.bind_tools(tools=available_tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

# chat node
def chatbot(state: State):
    user_message = state["messages"][-1].content
    relevant_memories = mem_client.search(
    query=user_message,
    user_id="raj"
)
    memories = [f"ID: {mem.get('id')} Memory: {mem.get('memory')}" for mem in relevant_memories.get("results")]
    system_prompt = prompt(memories)
    response = llm_with_tools.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


# tool node
tool_node = ToolNode(tools=available_tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)  # chat node
graph_builder.add_node("tools", tool_node)  # tool node

graph_builder.add_edge(START, "chatbot")  # edges
graph_builder.add_conditional_edges("chatbot", tools_condition)  # conditional edge
graph_builder.add_edge("tools", "chatbot")
# graph_builder.add_edge("chatbot",END)  # we dont need to write this sh!t

graph = graph_builder.compile()
