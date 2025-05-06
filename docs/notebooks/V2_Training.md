# Step 4
## Prompt Training 2.0 notebook:
**Goal**: Develop a stronger dataset and better fine tuned model for prompt engineering
- This notebook references the ShareGPT 52k dataset

### Setup
- Remove preselected testing messages from dataset ('../data/ShareGPT/testing_prompts_cleaned')
- Take only the first messages in the each conversation (Same as before)

### Widget 1 & 2 - Prompt sampling & seperating
- **Goal**: Refine data quality and seperate large prompts for better tuning
- Created a widget to allow for manually seperating 'instructions' from 'context'
- Ran this on a random sample of prompts for the validation and train set, then also used the randomly preselected test set
- **Context**: 
  Rigid 'rules' or examples given to the prompt. Things that you want to have left unchanged in the prompt engineering, 
  but may give valuable insight into the problem.
  - Examples: code, a general school problem, or an article. 
- **Instruction**: 
  Portion of the prompt that is to be 'engineered', stating specific 
  instructions and arbitrary rules and suggestions for the model to specify its output.  
  - Examples: given a certain role for the model to play, saying 'summarize' or 'debug this', and any things that tell the model what to do directly
- Widget allowed for easy manual selection by copy-pasting the continous substring of the context into a box, in which the widget would recongize the rest of the string as the instruction
- **Statistics**:
  - 999 prompts seperated manually for the training set
  - 235 prompts seperated manually for the validation set
  - 963 prompts seperated manually for the testing set

### Prompt Generation
- For overall idea, reference Prompt_Training.txt
- For this iteration, we treat the original user prompt as the 'bad prompt', with no classification of type, technique, or anything else
- Then, we prompt most powerful model that we have access to (gemini-2.5-pro-preview-3-25), with the following:
  ```python
  '''
  You are a prompt engineering expert.

  Your task is to rewrite the instruction below using advanced prompt engineering techniques. If context is provided, use it as *background knowledge* to better understand the task — but do not include it in the final output.

  Guidelines:
  - Enhance the instruction to be clearer, more specific, and more effective
  - Use any prompting technique that best fits
  - Ground your rewrite in the provided context, if applicable
  - Do NOT copy or reference the context in your rewritten instruction

  Context:
  {context}

  Original Instruction:
  {instruction}

  Output ONLY the improved instruction without any additional text, explanations, or acknowledgments.
  Improved Instruction:
  '''
  ```

### Post Processing:
- Look for verbosity flags such as 'Improved Prompts'
- Remove substrings from obviously verbose prompts
