# Overview
This repo is buit to learn and practice use of model and how to build agentic ai.

# Prerequisites
We need to install
**TODO** - link to the WSL-setup repo

# Steps to download LLama
Follow the step llama website

## Convert Lama model to other format
<details>
  <summary>Usefull Info/Questions</summary>
❓**Why we need to change model to diffrent format? e.g guff, ggml or hugging face transform supported**

- **Optimization**: Different formats optimize models for specific hardware (CPUs, GPUs) and software, improving performance and efficiency.

- **Compatibility**:  Converting formats ensures models work seamlessly with various tools, libraries, and platforms.

- **Quantization**: Formats like GGUF/GGML support efficient quantization, reducing model size and memory usage for improved performance.

- While format conversion is crucial for local LLM running, it can also be necessary in cloud environments to ensure compatibility, optimization, and integration with cloud-specific tools and services.

❓**What is the diffrence btween pth vs pkl?**

- The .pth file format is a common way to save and load PyTorch models. It's like a snapshot of the model's architecture and learned parameters, allowing you to store and reuse the model later without retraining.
- Use .pkl for saving general Python objects, including models from other frameworks or data structures.

</details>

1. Convert the Llama model to HF model type
    This is another useful link to use [Hugging Face Llama](https://huggingface.co/docs/transformers/main/en/model_doc/llama3)

    ```sh
    # This worked fine but we can use Llama3.1-8B as directly it is big and memory intensive, it does work Ollama
    python3 ~/miniforge3/envs/cuda12-2/lib/python3.1/site-packages/transformers/models/llama/convert_llama_weights_to_hf.py \
    --input_dir /home/sanjay/.llama/checkpoints/Llama3.1-8B \
    --model_size 1B  \
    --output_dir /home/sanjay/.llama/checkpoints/Llama3.1-8B/hf-output/ \
    --llama_version 3.2

    # OR Converting 3.2 1B as small one
    python3 ~/miniforge3/envs/cuda12-2/lib/python3.1/site-packages/transformers/models/llama/convert_llama_weights_to_hf.py \
    --input_dir ~/.llama/checkpoints/Llama3.2-1B \
    --model_size 1B  \
    --output_dir ~/.llama/checkpoints/Llama3.2-1B/hf-output/ \
    --llama_version 3.2
    ```

2. To use LangChain or specifically llama.cpp we need to convert it to GGUF
    - Clone the Repo https://github.com/ggerganov/llama.cpp/tree/master
    - Install the Python dependency (Always remember to create a separate environment to do this)

    ```sh
    python convert_hf_to_gguf.py /home/sanjay-dev/.llama/checkpoints/Llama3.2-1B/hf-output --outfile /home/sanjay-dev/.llama/checkpoints/Llama3.2-1B/hf-output/model.gguf --outtype f16
    ```

## Ways to run the LLM
This exmaple we are using LLama3.2:1B model in three way
### 1. Using ollama
This is one of the fasted way to run the llama model and play it localy. 
To intall the Ollama: [https://ollama.com/download/linux](https://ollama.com/download/linux)

Find the available models from [Ollaman model search](https://ollama.com/search) page

```sh
# To pull the modle
ollama pull llama3.2:1b

# To list the modeles availble
ollama ls

# To run the model
ollama run llama3.2:1b
``` 

### 2. Using HF Transforms (Locally downloaded Llama)
....
### 3. Using llama.cpp in Langchain
....
