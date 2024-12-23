 
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# # Tell CUDA to use the second GPU (index 1)
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# # Make PyTorch use the new CUDA configuration.
# import torch
# # Ensure that GPU is available
# if torch.cuda.is_available():
#     print("GPU is available")
#     print(torch.cuda.get_device_name(0))  # Print the name of the GPU
# else:
#     print("GPU is not available")
# # Set environment variable (optional, but recommended)
# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


model_path = "/home/sanjay-dev/.llama/checkpoints/Llama3.2-1B/hf-output/"  # Path to the converted model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

generator = pipeline(task="text2text-generation", model=model, tokenizer=tokenizer) 

# Generate text
prompt = "What is the capital of France?"
output = generator(prompt)
print(output)  # Access the generated text

