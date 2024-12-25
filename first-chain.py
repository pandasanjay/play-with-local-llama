from langchain_core.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

import re

# Initialize the Llama 2 model
llm = LlamaCpp(
    model_path="/home/sanjay-dev/.llama/checkpoints/Llama3.2-1B/hf-output/model.gguf",
    n_ctx=2048,
    n_gpu_layers=1,  # Offload 1 layer to the GPU
    verbose=False,
    chat_format="llama-2"
    
)

prompt = ChatPromptTemplate.from_messages(
    [("user", "Tell me a {adjective} joke")],
)

# Create the chain using the new syntax
chain = prompt | llm | StrOutputParser()
outer_chain = RunnablePassthrough().assign(text=chain)
# Execute the chain
text = "Hello, how are you?"
result = outer_chain.invoke({"adjective": "funny"})

# Print the result
print(result)