# Step 2
## ShareGPT Notebook / Dataset:
**Goal**: Procure a dataset 

### Dataset
- This dataset was referenced from a scraped dataset available on hugging face
- Populated from an old platform called 'shareGPT' that was used to share chat gpt conversations
- Must be manually converted to a Dataframe, as it was just an 'iterable object'
- Total conversations: 52180

### Preprocessing
- Used LangDetect library to disclude the non-english conversations
  - Remaining Conversations: 34969
- Extract only human messages, as the conversations include ChatGPT outputs
  - Remaining Prompts (From conversations): 198541
  - Saved to '../data/shareGPT/unfiltered_english_prompts.csv'
- Extract only first prompt from conversation - avoids contexted being needed with a prompt
  - Remaining Prompts: 34920
- Filter prompts that are fewer than 3 words
- Save to '../data/ShareGPT/testing_prompts_cleaned'