from typing import Annotated
from langchain_google_community import GoogleSearchResults
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import requests
from dotenv import load_dotenv
import os
from langchain.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.schema import AIMessage, HumanMessage
from IPython.display import Image, display
import os
import cv2
import numpy as np
from scrapper import scraping, is_valid_url


# Load environment variables
load_dotenv()

os.environ["GOOGLE_API_KEY"] = "AIzaSyC3zng47L2XpyC2hssZBEM2x0i31amcedw"
os.environ["GOOGLE_CSE_ID"] = "a1fc75b9834eb4b60"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBKW14k66Vsr8s5bfaXcTXB7dshJE7-22U"

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    


graph_builder = StateGraph(State)

# llm = ChatGoogleGenerativeAI()
# print(llm.list_models())
# exit(0)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
search = GoogleSearchAPIWrapper()
search_tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)


def chatbot(state: State):
    print("LLM State: ", state['messages'][-1])
    val = "2 are very serious but 1 is funny. Write a short story about it"
    state['messages'] =  [HumanMessage(content=f'the dragon has 3 heads. {val}')]
    # print("LLM State: ", state['messages'])
    return {"messages": [llm.invoke(state["messages"])]}



# def search(state: State):
#     user_query = state["messages"][-1].content  
#     search_results = search_tool.run(user_query) 
#     # print("OK1")
#     # If the result is a string, wrap it in a list
#     if isinstance(search_results, str):
#         search_results = [search_results]
#     return {"messages": state["messages"] + [AIMessage(content="\n".join(search_results))]}   


# def scrape_reviews(state: State):
#     url = state["messages"][-1].content
#     reviews = scraping(url)

#     return {"messages": state["messages"] + [AIMessage(content="\n".join(reviews))]}



# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
# graph_builder.add_node("search", search)

# Set the entry point of the graph
# graph_builder.set_entry_point("router")

graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("router", "chatbot")
# graph_builder.add_edge("router", "search")

# graph_builder.add_edge("s", END)
# graph_builder.add_edge("chatbot", 'search')
graph_builder.add_edge("chatbot", END)


graph = graph_builder.compile()



try:
    # Generate the Mermaid diagram and save it as a PNG
    graph_image = graph.get_graph().draw_mermaid_png()
    
    # Save the PNG data to a file
    temp_file = "graph.png"
    with open(temp_file, "wb") as f:
        f.write(graph_image)
    
    # Read and display the image using OpenCV
    img = cv2.imread(temp_file)
    cv2.imshow('Graph Visualization', img)
    cv2.waitKey(0)  # Wait for any key press
    cv2.destroyAllWindows()  # Close the window
    
    # Cleanup the temporary file
    os.remove(temp_file)
    
except Exception as e:
    print(f"Failed to display graph: {e}")
    pass

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        # user_input = "Reviews: " + user_input
        if is_valid_url(user_input):
            stream_graph_updates(user_input)
        else:
            stream_graph_updates(user_input)

    except Exception as e:
        print(f"Error: {e}")    
        break
