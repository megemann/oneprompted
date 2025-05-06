# Step 6
## Responses notebook:
**Goal**: Gather all improved prompts and responses for all models for later evaluation

### Setup
- Load test data, and connect free API_KEY as well as a tier 1 for payment

### Dataset
- For testing purposes, we used the sampled and cleaned testing set from 'Prompt_Training_2.0'

### Specifications
- When referring to the 'base untuned model', it corresponds to 'gemini-2.0-flash-lite-001', which is the compact but fine-tunable model available in vertex AI
- When referring to the 'Gemini model', it corresponds to 'gemini-2.0-flash', commonly available via the Google API 

### Prompt Improvements
To gather an accurate sample of the data, there are 4 classes I wanted to evaluate:

1. **No model Response**: Control, no model improvement
2. **Base Model Responses**: Feed the original prompt from the testing set into the base untuned model
3. **Fine Tuned V1 Responses**: Feed the original prompt into the initial fine tuned model
   
   Prompt for both 2 and 3:
   ```
   You are a prompt engineering expert that transforms simple 
   prompts into more effective versions. Analyze the input prompt and create
   an improved version that includes specific details, context, desired output format, 
   and any relevant constraints. Make the prompt clear, specific, and designed to 
   generate high-quality responses.
   
   Input Prompt: {prompt}

   Respond ONLY with the text of the improved prompt, without any explanations, 
   introductions, or additional commentary.
   ```

4. **Fine Tuned V2 Responses**: Feed the original separated instruction and context into the updated fine tuned model
   
   Prompt for 4:
   ```
   You are a prompt engineering expert.

   Your task is to rewrite the instruction below using advanced prompt engineering techniques. 
   If context is provided, use it as *background knowledge* to better understand the task — but do not include it in the final output.

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
   ```

**DISCLAIMER**: Due to training differences, these models are prompted differently, which could indirectly lead to variance.
However, the V2 of the fine tuned model is refined differently, and will take input differently, so it is necessary even though it could disrupt the integrity of the study.

**NOTE**: The overall text fed into the models is the same, the ONLY difference is that the context was manually separated as to be given different discretion, while the 
other models received the entire prompt as a big block. When experimenting with this, we found an issue in the necessary context getting altered by the LLM, resulting
in this solution.

### Outputs
1. **No model response**: Simply prompt Gemini with the 'original prompt' from the dataset
2-3. **Fine Tuned V1 and Base Model**: Prompt with the improved prompt and record the response
4. **Fine Tuned V2 response**: Prompt with the context appended onto the end of the fine tuned instruction.
