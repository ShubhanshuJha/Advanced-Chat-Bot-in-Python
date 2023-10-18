# import os
import openai
from langchain.utilities import WikipediaAPIWrapper
from langchain import OpenAI
from langchain import PromptTemplate
import os 
from dotenv import find_dotenv, load_dotenv

# with open("API_KEY", "r") as f:
#     openai.api_key = f.read().strip()
MODEL_ENGINE = "text-davinci-002"

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

question = "who is naruto"


def wiki_answer(question):
    wiki = WikipediaAPIWrapper()

    llm = OpenAI(temperature=0.5)
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


print(wiki_answer(question))


def generate_answer(question):
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
