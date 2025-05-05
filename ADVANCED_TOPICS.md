# Advanced LLM Topics: Understanding Models and Fine-Tuning

This directory contains examples and notebooks for exploring more advanced concepts related to Large Language Models (LLMs).

## Understanding Model Internals

The `tokenizers/` and `transformers/` directories contain resources to help you understand how LLMs work internally:

### Tokenizers
Tokenization is the process of converting text into tokens that models can process:

- [helloworld_tokenizers.ipynb](../tokenizers/helloworld_tokenizers.ipynb): Introduction to tokenization
- [visualise_tokenization.py](../tokenizers/visualise_tokenization.py): Visual representation of how text is tokenized
- [explore_model.ipynb](../tokenizers/explore_model.ipynb): Exploring token embeddings in models

### Transformers
Transformer architecture is the foundation of modern LLMs:

- [self_attention.ipynb](../tokenizers/self_attention.ipynb): Understanding the self-attention mechanism
- [multi_head_attention.ipynb](../tokenizers/multi_head_attention.ipynb): How multi-head attention works

## Fine-Tuning Models

Fine-tuning involves adapting pre-trained models for specific tasks:

- [hf_guide_image_clacification_loRa.ipynb](../fine-tuning/hf_guide_image_clacification_loRa.ipynb): Example of fine-tuning using LoRA (Low-Rank Adaptation)

## Key Concepts

### Tokenization
- **Vocabulary**: The set of tokens a model knows
- **Subword Tokenization**: Breaking words into smaller units
- **Special Tokens**: Tokens with special meaning (e.g., [START], [END])

### Transformer Architecture
- **Self-Attention**: How tokens relate to each other
- **Feed-Forward Networks**: Processing token representations
- **Positional Encoding**: Capturing token positions

### Fine-Tuning Techniques
- **Full Fine-Tuning**: Updating all model parameters
- **Parameter-Efficient Fine-Tuning**: Updating only a subset of parameters
  - **LoRA**: Low-Rank Adaptation
  - **Prompt Tuning**: Learning optimal prompts

## Learning Path

1. Start by understanding tokenization using the tokenizers notebooks
2. Move on to self-attention and multi-head attention
3. Explore model architecture in more detail
4. Learn about fine-tuning techniques
5. Experiment with fine-tuning your own models

## Resources

- [Hugging Face Documentation](https://huggingface.co/docs)
- [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [Andrej Karpathy's Let's Build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY)