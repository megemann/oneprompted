# OnePrompted

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Vertex AI](https://img.shields.io/badge/VertexAI-Powered-green.svg)](https://cloud.google.com/vertex-ai)
[![Gemini](https://img.shields.io/badge/Gemini-2.0-orange.svg)](https://deepmind.google/technologies/gemini/)

<h3>Teaching AI to improve your prompts - automatically.</h3>

[Blog Post](docs/BlogPost.md) | [API Documentation](docs/api.md) | [Usage Demo](images/V2/Usage.mp4)

![Project Banner Image - Include an image of improved prompts visualization here](https://i.postimg.cc/SxZry8Zj/One-Prompted-banner.png)

</div>

## 🚀 Overview

OnePrompted is an AI system that enhances your prompts before sending them to large language models. We built a fine-tuned model that takes vague, simple prompts and transforms them into highly effective ones using advanced prompt engineering techniques.

### 💡 The Problem

Prompts are the new programming language—but most people don't know how to write effective ones. Even the most powerful AI models can't produce great results from poorly formulated prompts.

### 🔍 Our Solution

Instead of requiring users to learn prompt engineering techniques, we trained a custom Gen AI model to automatically enhance prompts before they reach the main model, significantly improving the quality of responses.

## ✨ Features

- **Automatic Prompt Enhancement**: Transforms simple prompts into structured, detailed instructions
- **Context-Aware Improvement**: Separates instructions from context for better grounding
- **Fast Processing**: Lightweight model optimized for quick processing
- **Easy Integration**: Simple REST API for integration with any application

## 🔧 Technical Details

### Technology Stack

- **Vertex AI**: For model fine-tuning and deployment
- **Gemini 2.0**: Base model for knowledge distillation
- **FastAPI**: Backend framework for API endpoints
- **Firestore**: For request tracking and rate limiting
- **Docker**: For containerized deployment

### Key Approaches

- **Knowledge Distillation**: Training a smaller model on outputs from larger models
- **Prompt Separation**: Distinguishing between instructions and context
- **Grounding**: Ensuring the model stays anchored to provided context

## 📊 Results

Our fine-tuned model outperformed competing approaches in pairwise evaluations:

<div align="center">

![Pairwise Evaluation Results - Include a chart showing comparative performance](https://i.postimg.cc/VkgGBjSR/Pairwise-overall.png)

</div>

Key findings:
- 18% higher win rate in direct comparisons with other approaches
- Consistent performance across varying prompt lengths
- Significant improvements in response quality and relevance

## 🔌 API Usage

The OnePrompted API allows simple integration with your applications:

```bash
curl -X POST https://api.oneprompted.com/generate \
  -H "Content-Type: application/json" \
  -d '{"input": "Write a blog post about machine learning"}'
```

Response:
```json
{
  "output": "Compose a comprehensive 800-1000 word blog post titled 'The Evolution and Future of Machine Learning: From Theory to Practice.' Structure the post with the following sections: 1) An introduction explaining what machine learning is and its significance in today's technological landscape; 2) A brief history of machine learning, highlighting key milestones and breakthroughs; 3) Current real-world applications across 3-4 diverse industries; 4) Challenges and ethical considerations; 5) Future trends and predictions for the next 5 years; and 6) A conclusion with actionable insights for businesses considering implementing ML solutions. Include relevant statistics, examples, and maintain an informative yet accessible tone suitable for a technically curious but non-expert audience."
}
```

See [API Documentation](docs/api.md) for more details.

## 📂 Project Structure

```
oneprompted/
├── api/
│   └── generate/            # API implementation
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
├── data/                    # Datasets and model responses
│   ├── Prompt_Training_V1/  # V1 training data
│   ├── Prompt_Training_V2/  # V2 training data
│   ├── PromptEval/          # Evaluation datasets
│   ├── Responses/           # Model responses
│   ├── ShareGPT/            # ShareGPT dataset
│   └── Responses.zip        # Archived responses
├── docs/                    # Documentation
│   ├── data/                # Dataset documentation
│   │   ├── Evaluation.md
│   │   ├── Responses.md
│   │   ├── ShareGPT.md
│   │   ├── V1.md
│   │   └── V2.md
│   ├── notebooks/           # Notebook documentation
│   │   ├── Fine_Tuning.md
│   │   ├── Responses.md
│   │   ├── ShareGPT.md
│   │   ├── V1_Training.md
│   │   └── V2_Training.md
│   ├── api.md               # API documentation
│   ├── BlogPost.md          # Project blog post
│   └── Goals.md             # Project goals
├── images/                  # Project images
│   ├── Evaluation/          # Evaluation visualizations
│   ├── V1/                  # V1 model visualizations
│   ├── V2/                  # V2 model visualizations
│   └── OnePrompted_banner.png # Project banner
└── notebooks/              # Jupyter notebooks
    ├── dev_notebooks/      # Development notebooks
    │   ├── Eval_Clean.ipynb
    │   ├── Responses_Clean.ipynb
    │   ├── Share_GPT.ipynb
    │   ├── V1_Training.ipynb
    │   └── V2_Training.ipynb
    └── .gitignore
```

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+
- Google Cloud account with Vertex AI access
- Docker (for deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/megemann/oneprompted.git
   cd oneprompted
   ```

2. Install dependencies:
   ```bash
   pip install -r api/generate/requirements.txt
   ```

3. Set up your environment:
   ```bash
   # Create env.json with your Google Cloud credentials
   ```

4. Run the API locally:
   ```bash
   cd api/generate
   uvicorn main:app --reload
   ```

### Deployment

Deploy using Docker:

```bash
cd api/generate
docker build -t oneprompted-api .
docker run -p 8080:8080 oneprompted-api
```

## 🔮 Future Work

- Lightweight, portable assistant for prompt optimization
- Intelligent LLM provider selection based on prompt category
- Embedding-based semantic search for similar high-quality prompts
- Enhanced context handling for code and document prompts

## 👥 Authors

**Austin Fairbanks** | [ajfairbanks.me](https://ajfairbanks.me)  
*University of Massachusetts Amherst*

**Ian Rapko** | [iann.dev](https://iann.dev)  
*University of Massachusetts Amherst*

## 📬 Connect With Us

- [**Twitter**](https://twitter.com/ajfairbanksML) - Follow for updates
- [**LinkedIn**](https://linkedin.com/in/ajf2005) - Connect professionally
- [**GitHub**](https://github.com/megemann) - Check out our code
- [**Email**](mailto:ajfairbanks2005@gmail.com) - Reach out directly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
