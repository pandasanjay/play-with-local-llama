# Oveview 
We are budiling a task manager descktop application, agentic AI used to lean and help you to be more productive.

# PRE REQUISIT
We need to install

## Python env

1- Create a python env
```
python3 -m venv llama-env
// Activate 
source llama-env/bin/activate
```
2- Convert the llama model to hf model
This is another usefull link to use [Hugging Face Llama](https://huggingface.co/docs/transformers/main/en/model_doc/llama3)

```sh
# This worked fine but we can use Llama3.1-8B as directly it is big and memeory intencive, it does work Ollama
python3 ~/miniforge3/envs/cuda12-2/lib/python3.1/site-packages/transformers/models/llama/convert_llama_weights_to_hf.py \
--input_dir /home/sanjay/.llama/checkpoints/Llama3.1-8B \
--model_size 1B  \
--output_dir /home/sanjay/.llama/checkpoints/Llama3.1-8B/hf-output/ \
--llama_version 3.2

#OR  Converting 3.2 1B as small one
python3 ~/miniforge3/envs/cuda12-2/lib/python3.1/site-packages/transformers/models/llama/convert_llama_weights_to_hf.py \
--input_dir ~/.llama/checkpoints/Llama3.2-1B \
--model_size 1B  \
--output_dir ~/.llama/checkpoints/Llama3.2-1B/hf-output/ \
--llama_version 3.2

```

