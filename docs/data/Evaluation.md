# PromptEval Datacards

## train_logreg.joblib

**Description**: Serialized machine learning model that classifies prompts as "good" or "bad".

**Contents**:
- TF-IDF vectorizer: Transforms prompts into numerical features
- Logistic Regression classifier: Trained to predict prompt quality
- Model parameters: Hyperparameters used during training

**Creation Process**:
- Manually labeled ~200 prompts as good/bad
- Transformed text using TF-IDF vectorization (n-grams of 1-2 words)
- Trained logistic regression model with 2000 max iterations
- Serialized with joblib for persistence

**Usage**: Used to automatically evaluate prompts with a probability score (0-1) of being a "good" prompt.

**Limitations**: Evaluates based on word patterns only, without understanding semantic meaning.

## prompt_eval_scores.csv

**Description**: Evaluation scores for prompts from different model variants.

**Columns**:
- original_prompt: The input prompt text
- model: Model variant that produced the response ("none", "v1", "v2", "base")
- score: Probability (0-1) from logistic regression that the prompt is "good"

**Creation Process**:
- Processed each prompt variant through the trained logistic regression
- Assigned quality scores based on probability outputs
- Compiled results across all model variants

**Usage**: Used for comparative analysis to determine which model produces better prompts.

## newRubric.csv

**Description**: Extended evaluation with robust multi-category assessment.

**Columns**:
- prompt: Original prompt text
- model: Model variant identifier ("none", "v1", "v2", "base")
- lr_score: Logistic regression score (0-1)
- rubric_score: Weighted composite score from Gemini evaluation
- task_category: Classification of prompt type (Informational/Creative/Technical/Problem-solving/Analytical)
- relevance, accuracy, completeness, clarity, creativity, conciseness, technical_correctness, actionability: Individual category scores (1-5 scale)

**Creation Process**:
- Selected prompt samples for detailed evaluation
- Used Gemini to assess prompts across multiple dimensions
- Applied category-specific weighting formulas for composite scores

**Usage**: Provides nuanced, multi-dimensional evaluation of prompt quality beyond binary classification.

## prompt_eval_rubric.csv

**Description**: Detailed rubric-based evaluations for prompt quality assessment.

**Columns**:
- Similar to newRubric.csv but with potentially different samples or evaluation parameters
- Contains structured evaluation data from LLM-based assessment

**Creation Process**:
- Utilized Gemini to evaluate prompts against a standardized rubric
- Structured output as JSON with consistent evaluation criteria
- Extracted and normalized scores across evaluation dimensions

**Usage**: Used to identify strengths and weaknesses in different prompt formulations.

## responses_sample_scores.csv

**Description**: Evaluation scores for model responses rather than the prompts themselves.

**Columns**:
- original_prompt: Input prompt text
- model: Model variant identifier
- score: Quality score of the response (not the prompt)

**Creation Process**:
- Sampled 50 prompts with random seed 42
- Generated responses using different model variants
- Evaluated response quality using Gemini rubric
- Scored each response-variant pair

**Usage**: Assesses the quality of outputs rather than inputs, providing insight into which model generates the best responses regardless of prompt quality.

## pairwise_results.csv

**Description**: Direct comparison between pairs of model responses.

**Columns**:
- original_prompt: The input prompt text
- variant_a: First model being compared
- variant_b: Second model being compared
- choice: Which response was better ("A" or "B")

**Creation Process**:
- Sampled 200 prompts with random seed 42
- Generated pairs of model variants to compare
- Used Gemini to directly evaluate which response was better
- Recorded binary A/B decisions for each comparison

**Usage**: Provides direct competitive evaluation without the ambiguity of numerical scoring systems, showing which models consistently produce better responses.

## graded_responses.csv

**Description**: Comprehensive graded evaluation of response quality.

**Columns**:
- Similar structure to other evaluation files
- Contains model identifiers, response text, and quality assessments

**Creation Process**:
- Compiled responses from various models
- Applied consistent grading methodology (likely a combination of automated and LLM-based evaluation)
- Normalized scores for comparison purposes

**Usage**: Allows for holistic analysis of response quality across different models and prompt types.