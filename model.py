# import os
import openai
from langchain.utilities import WikipediaAPIWrapper
from langchain import OpenAI
from langchain import PromptTemplate
import os 
from dotenv import find_dotenv, load_dotenv
from langchain.utilities import PythonREPL
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.agents import initialize_agent

# with open("API_KEY", "r") as f:
#     openai.api_key = f.read().strip()
MODEL_ENGINE = "text-davinci-002"

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

question = "Who won the fight between Logan Paul and Dillon Danis And How?"

llm = OpenAI(temperature=0.5)

def ask_wiki(question):
    wiki = WikipediaAPIWrapper()


    result = wiki.run(question)
    template = """
    Please write a concise and to the point summary, make it easy to understand, include all important points from the following text:
    {result}
    Write only those points whhich are related to the {question}
"""
    prompt = PromptTemplate(input_variables=["result","question"], template=template)
    summary_prompt = prompt.format(result=result,question=question)
    summary = llm(summary_prompt)

    return summary


def ask_REPL(question):
    python_repl = PythonREPL()
    result = python_repl.run(question)
    return result


def ask_web(question):
    search = DuckDuckGoSearchRun()
    result = search.run(question)

    template = """
    Please write a concise and to the point summary, easy to understand, include all important points from the following text:
    {result}
    Write only those points which are related to the {question}
    Do NOT write unrelated points
"""
    prompt = PromptTemplate(input_variables=["result","question"], template=template)
    summary_prompt = prompt.format(result=result,question=question)
    summary = llm(summary_prompt)

    return summary


# print(ask_web(question))





def ask_openai(question):
    prompt = f"Question: {question}\n" "Answer:"
    completions = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    answer = message.strip().split("\nAnswer:")[-1].strip()
    return answer


tools = [
    Tool(
        name = "wikipedia",
        func= ask_wiki,
        description=" Useful when you need factual information about topics, concepts, events and people. on wikipedia"
    )
]

repl_tool = Tool(
    name='Python REPL',
    func= ask_REPL,
    description="useful for when you need to use python to answer a question. You should input python code"
    )

duckduckgo_tool = Tool(
    name='Web Search',
    func= ask_web,
    description="Useful for when you need to do a search on the internet to find information that another tool can't find, or when you need up-to-date factual information that goes beyond your existing knowledge. be specific with your input."
)

openai_tool = Tool(
    name="openai search",
    func= ask_openai,
    description='Useful when you need accurate and insightful answers to complex questions that go beyond factual information.'
)

tools.append(duckduckgo_tool)
tools.append(repl_tool)
tools.append(openai_tool)

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
)


answer = zero_shot_agent.run(question)
