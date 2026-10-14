import os

import streamlit as st
from langchain_groq import ChatGroq 
from dotenv import load_dotenv

# Legacy chain and agent components moved to langchain_classic
from langchain_classic.chains import LLMMathChain, LLMChain
from langchain_classic.agents import Tool, initialize_agent
from langchain_classic.agents.agent_types import AgentType

# Core & Community components 
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler 

load_dotenv()

##Setting up the streamlit app
st.set_page_config(page_title="Text to Math Problem Solver", page_icon=":robot:")
st.title("Text to Math Problem Solver Using GPT OSS 120B :robot:")

groq_api_key = st.sidebar.text_input(
    "Enter your Groq API Key",
    value=os.getenv("GROQ_API_KEY", ""),
    type="password",
)

if not groq_api_key:
    st.info("Please provide your Groq API Key to use the app.")
    st.stop()

language_model = ChatGroq(model="openai/gpt-oss-120b", groq_api_key=groq_api_key) ##This is LLM

## Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="Useful for when you need to answer questions about math or specific topics. Input should be a search query." 
)

## Initialze the Math tool
math_chain = LLMMathChain.from_llm(llm=language_model, verbose=True)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Useful for when you need to answer questions about math. Input should be a valid mathematical expression."
)

prompt = """
You are an agent tasked with solving math problems. Logically arrive at the final answer by using the tools provided.
Provide a step-by-step reasoning process, and ensure that the final answer is clearly stated at the end along with the detailed explanation.
If you need to look up information, use the Wikipedia tool. If you need to perform calculations, use the Calculator tool.
Always double-check your work before providing the final answer for the Question below.
Question:{question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combine all the tools into a chain
chain = LLMChain(llm=language_model, prompt=prompt_template, verbose=True)

reasoning_tool = Tool(
    name="Reasoning Tool",
    func=lambda q: chain.invoke({"question": q}),
    description="Useful for when you need to reason through a math problem step-by-step. Input should be a math problem in text form."
)

## Mathproblem solving agent
tools = [wikipedia_tool, calculator, reasoning_tool]
agent = initialize_agent(
    tools=tools,
    llm=language_model,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Math Problem Solver is ready! Please enter a math problem in text form, and I will help you solve it step-by-step."}
    ]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

## function to handle to generate response from the agent
def generate_response(user_input):
    chat_history = [
        HumanMessage(content=message["content"])
        if message["role"] == "user"
        else AIMessage(content=message["content"])
        for message in st.session_state.messages[:-1]
    ]
    response = agent.invoke({"input": user_input, "chat_history": chat_history})
    return response

## Lets start the interation with the user
user_input = st.text_area("Enter a math problem in text form...","What is the integration of x^2 + 3x + 2 with respect to x?")
if st.button("find my answer"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = generate_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response['output']})
            st.chat_message("assistant").write(response['output'])
    else:
        st.warning("Please enter a math problem to solve.")
