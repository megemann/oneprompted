# Project Goals and Pipeline

## Data Sources
- **ImprovePrompts** → ShareGPT (preprocessed dataset)
- **Data/ShareGPT** → Unfiltered English Prompts (english questions)
- **Testing Prompts** → Testing set, prompt into LLM, used to test how well it improves the prompts
- **Basic Prompts responses** → Fed unimproved prompts into Gemini and has response

## Notebooks
### Prompt Training Notebook
- LLM Generated prompts, good vs bad, and categories

### Responses Notebook
- Fed fine tuned model and base model and original prompts
- Outputs a better prompt for each of them (prompt engineering)
- Takes responses and outputs responses of each into flash2.0 responses and fine tuned responses

## Overall Goal
These prompts are what a general person would say. We want to finely pick through a data set, say how we make it better. Do it for a general prompt instead of a LLM prompt.

## Pipeline
1. Take ShareGPT data, preprocess and filter it out to get a good dataset
2. Ask model to generate improved prompts of this dataset
3. Use Prompt-training dataset as the template for distinguishing good vs bad prompts and categorize the way/method of calling
4. In Responses, feed in all 3 models and output a better prompt for each of them
5. Take responses and compare with each other in a grader/rubric to see what ways to improve the most for the specific category

## Project Steps
### FIRST STEP:
On the fly prompt engineering to improving response.

### SECOND STEP:
Classifying prompts for what model is the best.