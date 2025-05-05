 
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_path = "/home/sanjay-dev/.llama/checkpoints/Llama3.2-1B/hf-output/"  # Path to the converted model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

generator = pipeline(task="text2text-generation", model=model, tokenizer=tokenizer) 

# Generate text
prompt = "What is the capital of France?"
output = generator(prompt)
print(output)  # Access the generated text

