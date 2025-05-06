# ShareGPT Dataset

## Overview
The ShareGPT dataset contains conversations between users and ChatGPT, scraped from the ShareGPT platform where users shared their interactions. This dataset serves as a foundation for our prompt engineering and improvement models.

## Dataset Characteristics
- **Source**: Scraped dataset available on Hugging Face
- **Original Size**: 52,180 conversations
- **Format**: Converted from iterable object to structured DataFrame

## Preprocessing Steps
1. **Language Filtering**:
   - Applied LangDetect library to retain only English conversations
   - Reduced to 34,969 conversations (67% of original)

2. **Message Extraction**:
   - Isolated human messages from the conversations
   - Extracted 198,541 total prompts
   - Stored in '../data/shareGPT/unfiltered_english_prompts.csv'

3. **Context Removal**:
   - Selected only the first prompt from each conversation to eliminate dependency on prior context
   - Resulted in 34,920 independent prompts

4. **Quality Filtering**:
   - Removed prompts with fewer than 3 words
   - Final dataset saved to '../data/ShareGPT/testing_prompts_cleaned'

## Usage
This dataset provides a diverse collection of real-world prompts that serve as the foundation for training our prompt improvement models, particularly for the V2 fine-tuned model.

## testing_prompts_cleaned.csv

This file contains the cleaned, filtered prompts extracted from the ShareGPT dataset.

### File Structure
- **original_id**: Unique identifier for each prompt
- **original_prompt**: The raw text of the user's prompt

## unfiltered_english_prompts.csv
### File Structure
- **conversation_id**: Unique identifier for the conversation
- **prompt**: The text of the user's message
- **prompt_length**: Character count of the prompt

