from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


template = '''
Answer to the questions and start by saying my name: Khushbakht
Question: {question}
Answer:
'''

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

result = chain.invoke({"question": "hey how are you"})
print(result)