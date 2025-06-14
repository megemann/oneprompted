# Step 1
## Prompt Training notebook:
**Goal**: Generate data for a prompt engineering dataset so that we could take that data and fine tune a separate model

### Setup
- Gathered a list of prompting techniques to select from
- Tried to categorize 'types of prompts' in order to balance over the full domain
- Created a class for a 'prompt example' - generation later
  ```python
  class PromptExample(BaseModel):
      task_description: str  # Description of the task that the generated prompt would be on
      complexity: str = Field(..., pattern="^(low|medium|high)$")  # Complexity of the task
      bad_prompt: str  # Generated 'bad' prompt
      good_prompt: str  # Generated 'good' prompt
      expected_answer: str  # Outline of the 'expected answer' for a prompt - to ensure it remained on task
      prompting_techniques: List[PromptingTechnique]  # List of prompting techniques used to generate the prompt for the given task
      prompt_type: PromptType  # Categorized prompt
      notes: Optional[str] = None  # Extra notes or observations about the example
  ```
- `prompt_type_to_techniques` - arbitrarily generated list made by selecting the predicted top 3 types of techniques that would best suit each type of prompting classification

### Prompting Building
- prompt:
  ```python
  return f"""
      You are a prompt engineering assistant.

      TASK: {task_description}
      COMPLEXITY: {complexity}

      1. Generate a bad prompt that would likely get a weak or vague answer.
      2. Generate an improved prompt that uses one or more prompting techniques, choosing the best techniques for the task, preferring the following list: {selected_techniques}
      3. Describe the expected answer (what an ideal output from an LLM would be).

      Return the result in JSON like this:
      {{
          "bad_prompt": "...",
          "good_prompt": "...",
          "expected_answer": "...",
          "prompting_techniques": ["..."]
      }}
      """.strip()
  ```
- Prompt structured in a way to take a task, and then generate a bad a good prompt for it to distinguish between in fine tuning
- `def query_gemini(prompt: str, max_retries=3)`: function that uses **STRUCTURED OUTPUT** to generate new data in a format. 
  - The format is:
    ```python
    class PromptExampleResponse(typing.TypedDict):
        bad_prompt: str
        good_prompt: str
        expected_answer: str
        prompting_techniques: list[str]
    ```

- `def create_prompt_example_with_schema(task_description: str, complexity: str, prompt_type: PromptType, max_attempts=3) -> Optional[PromptExample]`:
  - Wrapper around query gemini to ensure data Format

### Prompt Generation:
- Class Descriptions: 
  #### Complexity Distribution
  - **Medium complexity**: 50% (most common real-world case)
  - **Low complexity**: 25% (simpler tasks)
  - **High complexity**: 25% (challenging scenarios)

  #### Prompt Type Distribution
  Based on common usage patterns in AI interactions:

  ##### Higher frequency (10-15% each):
  - INFORMATIONAL (12%)
  - QUESTION_ANSWERING (12%)
  - INSTRUCTIONAL (10%)
  - SUMMARIZATION (10%)
  - ANALYSIS_CRITIQUE (8%)

  ##### Medium frequency (5-8% each):
  - PROGRAMMING_CODE_GENERATION (8%)
  - CREATIVE_WRITING (7%)
  - CONVERSATIONAL (7%)
  - COMPARISON (6%)
  - CODE_EXPLANATION (6%)

  ##### Lower frequency (2-5% each):
  - ROLE_PLAYING (5%)
  - DATA_EXTRACTION (5%)
  - STYLE_TONE_CHANGE (4%)
  - TRANSLATION (4%)
  - COMPLETION (3%)
  - CLASSIFICATION_TAGGING (3%)
- Prompt Type templates: AI generated static 'templates' to generate certain prompts in previously marked categories
  - Examples: 
    ```python
    {
        PromptType.INFORMATIONAL: [
            "Explain {topic} in {detail} detail",
            "Provide information about {topic}",
            "Describe how {topic} works",
            "Give a comprehensive overview of {topic}",
            "Share essential knowledge about {topic}"
        ],
        PromptType.QUESTION_ANSWERING: [
            "Answer questions about {topic}",
            "Respond to FAQs about {topic}",
            "Address common questions on {topic}",
            "Provide solutions to questions regarding {topic}",
            "Clarify inquiries related to {topic}"
        ],
        PromptType.INSTRUCTIONAL: [
            "Provide step-by-step instructions for {topic}",
            "Create a guide for {topic}",
            "Explain how to {topic}",
            "Develop a tutorial on {topic}",
            "Outline the process for {topic}"
        ], ...
    }
    ```

- Task: AI generated topics sorted by complexity:
  - Examples: 
    ```python
    topics = {
        "low": ["basic arithmetic", "primary colors", "simple recipes", "daily routines", 
                "weather patterns", "basic geography", "common animals", "popular sports",
                "household chores", "traffic signs", "telling time", "family relationships",
                "basic hygiene"],
        "medium": ["climate change", "renewable energy", "digital marketing", "healthy eating", 
                "financial planning", "machine learning basics", "world history", "psychology concepts",
                "interior design", "automotive maintenance", "social media strategy", "photography techniques",
                "public speaking"],
        "high": ["consciousness research", "cognitive architectures", "embodied cognition", "extended mind theory",
                "moral philosophy", "metaphysics", "epistemology", "philosophy of science",
                "philosophy of mind", "political philosophy", "bioethics", "neuroethics"]
    }
    ```

### PIPELINE
- Use function `def generate_examples(num_examples=1000)`:
  1. Select random task from the list, with the probability for complexity as stated prior (25,50,25)
  2. Select random Prompt Type based off of the probability distribution, Insert into random selection from possible tasks corresponding to the prompt type
  3. Feed task, complexity, and prompt type into create_prompt_example_with_schema
  4. Select corresponding prompting techniques based off of the prompt type: reference 1-2 of them
  5. Feed prompt into Gemini 2.0 Flash and receive:
     - Bad Prompt
     - Good Prompt
     - Prompting Techniques Used
     - Expected answer
  6. Repeat for num examples

### Analysis:
- Distributions:
  - Complexity distribution:
    ```
    complexity
    medium    731
    high      381
    low       338
    ```

  - Prompt type distribution:
    ```
    prompt_type
    INFORMATIONAL                  166
    QUESTION_ANSWERING             151
    PROGRAMMING_CODE_GENERATION    123
    SUMMARIZATION                  121
    INSTRUCTIONAL                  120
    ANALYSIS_CRITIQUE               98
    CONVERSATIONAL                  95
    COMPARISON                      91
    CREATIVE_WRITING                86
    CODE_EXPLANATION                76
    DATA_EXTRACTION                 71
    ROLE_PLAYING                    62
    TRANSLATION                     57
    STYLE_TONE_CHANGE               53
    COMPLETION                      46
    CLASSIFICATION_TAGGING          34
    ```

### PostProcessing: 
- Convert to JSONL file for Vertex AI fine tuning desired structure

### Final notes: 
Models at the beginning were for possible model selection algorithm
