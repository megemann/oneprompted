# Prompt Engineering & LLM Evaluation Toolkit

This repository contains three Jupyter notebooks designed to support research and experimentation with Large Language Models (LLMs), including benchmarking, prompt analysis, and fine-tuning datasets.

## Contents

### `Dataset.ipynb` – Model Benchmarks & Prompt Classification

This notebook focuses on defining and organizing benchmark data for various free-access LLMs and modeling different types of prompts.

#### Key Components:
- **Model Benchmark Dataset:** A list of LLMs (e.g., GPT-4o, Claude, Gemini) with metadata and performance scores on tasks like:
  - Reasoning
  - Coding
  - Data Analysis
  - Language Tasks
- **Ranking Visualization:** Function to sort and display models by task-specific scores.
- **Prompt Typing (uses `pydantic`):**
  - `PromptingTechnique`: Techniques like Chain-of-Thought, Role Prompting, Tree-of-Thoughts, etc.
  - `PromptType`: Task categories like Summarization, Code Generation, Role-Playing, etc.
  - `PromptExample`: Schema to compare bad vs good prompt examples using structured metadata.

---

### `Evaluations.ipynb` – Google Generative AI & Prompt Improvement

This notebook uses **Google Generative AI (Gemini)** and has prompt refinement strategies for model evaluation.

#### Key Components:
- **Environment Setup:** Loads keys from `env.json` to get API access to Google GenAI.
- **Model Listing:** Displays available Gemini models.
- **Prompt Refinement Function:** Uses Gemini to rewrite prompts with higher specificity, context, and clarity.
  - Example: Transforms “Explain AI to me like I’m a little kid” into a structured, high-quality prompt.

---

### `Improve_Prompts.ipynb` – Dataset Analysis (ShareGPT52K)

This notebook performs exploratory data analysis on the [ShareGPT52K](https://huggingface.co/datasets/RyokoAI/ShareGPT52K) dataset of multi-turn LLM conversations.

#### Key Components:
- **Streaming Load:** Efficiently loads the dataset via Hugging Face's streaming API.
- **Conversation Extraction:** Parses conversations and separates messages by role (e.g., user, assistant).
- **DataFrame Conversion:** Stores conversations in `pandas` dataframes for processing later down the line.
- **Conversation Statistics:** Generates the following from the dataset:
  - Message length distribution
  - Number of messages per dialog
  - Sample transcript previews

---

## Suggested Use Cases

- Evaluate and compare public LLM performance for specific tasks.
- Improve prompt quality using AI-enhanced transformations.
- Explore prompt engineering techniques and their outcomes.
- Analyze real-world prompt-response pairs for dataset refinement or fine-tuning.

---

## Dependencies

To use the notebooks, make sure you install:
```bash
pip install pandas datasets pydantic google-generativeai
