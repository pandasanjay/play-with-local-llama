from llama_cpp import Llama

# Path to your downloaded GGUF model
MODEL_PATH = "/path/to/your/model.gguf"

# Initialize the LLM
llm = Llama.from_pretrained(
    repo_id="QuantFactory/Llama-3.2-3B-GGUF",
    filename="Llama-3.2-3B.Q4_0.gguf",
    verbose=False
)

# Create a simple prompt
prompt = "Question: What is the capital of France? Answer:"

# Generate text
output = llm(
    prompt,
    max_tokens=32,  # Limit the response length
    stop=["Question:", "\n"],
    echo=True,
)

# Print the output
print(output)