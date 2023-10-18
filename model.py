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


# with open("API_KEY", "r") as f:
#     openai.api_key = f.read().strip()
MODEL_ENGINE = "text-davinci-002"

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

question = "Who won today's cwc match"

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
"""
    prompt = PromptTemplate(input_variables=["result","question"], template=template)
    summary_prompt = prompt.format(result=result,question=question)
    summary = llm(summary_prompt)

    return summary


print(ask_web(question))





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
        description="Useful for when you need to look up a topic, country or person on wikipedia"
    )
]