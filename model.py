# import os
import openai
from langchain.utilities import WikipediaAPIWrapper

with open("API_KEY", 'r') as f:
    openai.api_key = f.read().strip()
MODEL_ENGINE = "text-davinci-002"


question = "who is naruto"
def wiki_answer(question):
    wiki= WikipediaAPIWrapper()
    result = wiki.run(question)
    



print(wiki_answer(question))

def generate_answer(question):
    prompt = (f"Question: {question}\n"
              "Answer:")
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
