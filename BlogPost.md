# OnePrompted: Can AI Learn to Improve Your Prompts? We Built a Model to Try.

> We trained a custom Gen AI model to take vague, lazy prompts and turn them into highly effective ones using prompt engineering techniques. Here's how we did it using Vertex AI, Gemini, and a sprinkle of Gen AI magic. Code included. Lessons learned. Future unlocked.

---

## Table of Contents
- [OnePrompted: Can AI Learn to Improve Your Prompts? We Built a Model to Try.](#oneprompted-can-ai-learn-to-improve-your-prompts-we-built-a-model-to-try)
  - [Table of Contents](#table-of-contents)
  - [The Problem: Prompts Are the New Programming Language— But Most People Suck at It](#the-problem-prompts-are-the-new-programming-language-but-most-people-suck-at-it)
  - [Why Gen AI? Why Now?](#why-gen-ai-why-now)
  - [The Blueprint: Data, Model, and Pipeline](#the-blueprint-data-model-and-pipeline)
    - [The Dataset: Getting the prompts](#the-dataset-getting-the-prompts)
    - [The Model: Fine-Tuning with Vertex AI](#the-model-fine-tuning-with-vertex-ai)
    - [The Pipeline: Our Strategy in the kitchen](#the-pipeline-our-strategy-in-the-kitchen)
  - [Okay, but does this even do anything?](#okay-but-does-this-even-do-anything)
    - [Logistic Regression](#logistic-regression)
    - [Rubric Grading](#rubric-grading)
    - [Response Rubric Grading](#response-rubric-grading)
    - [Pairwise](#pairwise)
  - [Limitations \& Lessons Learned](#limitations--lessons-learned)
  - [The Future: Smarter Prompts, Smarter Users](#the-future-smarter-prompts-smarter-users)
  - [Wrapping Up: Prompt Engineering at the Edge](#wrapping-up-prompt-engineering-at-the-edge)
  - [📎 Appendix / Resources](#-appendix--resources)
  - [Authors](#authors)
  - [Connect With Me](#connect-with-me)

---

## The Problem: Prompts Are the New Programming Language— But Most People Suck at It

With the recent rise of Gemini, ChatGPT, and other Generative AI solutions, we have begun the era of maximal efficiency. Why not do even less? Instead of taking courses and spending hours learning difficult prompt engineering techniques to tailor to all species of models, why not let the models do some more heavy lifting!

---

## Why Gen AI? Why Now?

At a time when better and better models continue to be released with greater accuracy and increasing ability to solve harder problems, there seems to be almost no emphasis on helping these models _understand the input better_ before jumping to generation. We keep throwing massive models at vague, half-baked prompts and expecting magic.

But here's the thing: garbage in, garbage out still applies. A great model doesn't guarantee a great response if the prompt is unclear, incomplete, or poorly framed. That's where this project comes in; instead of trying to make the model even smarter, we focused on making the **prompt smarter** _before_ it reaches the model.

Gen AI isn't just about generation anymore, we now need to consider the optimizing all the other moving parts. And prompt optimization might just be one of the lowest-effort, highest-impact applications of it.

---

## The Blueprint: Data, Model, and Pipeline

Our goal was to take simple prompts from a source, process each using principled prompt-engineering strategies, and then label our data with our new and improved prompt to establish a clear supervised learning problem. With the use of fine tuning, we aim to develop a _efficient_ yet _effective_ middle-man that can be used to improve your prompt before feeding it to a larger model.

### The Dataset: Getting the prompts

After scouring the internet for hours and hours, going from dataset to dataset, we finally found our diamond in the rough: [ **ShareGPT52k**](https://huggingface.co/datasets/RyokoAI/ShareGPT52K) by RyokoAI. For some background, ShareGPT was an old 3rd party sharing service that allowed you to share your favorite ChatGPT conversations to your friends and family. This was perfect for our use-case, as we had access to a large sum of real human prompts given to models in the past, not mock data that we had to hope humans might actually prompt like.

After importing from the website, we were given data that looked like this:

```json
{
    "id": "2wtLdZm", # Conversation id
    "conversations": [ #list of prompts and responses, each assigned a role to distinguish them
        {
            "from": "human",
            "value": "Are you familiar with the SAS programming language?"
        },
        {
            "from": "gpt",
            "value": "<div class=\"markdown prose w-full break-words dark:prose-invert light\"><p>Yes, I am
            familiar with the SAS programming language. SAS is a statistical software suite that is widely used in
            data analysis, data management... (and so on)</p></div>"
        },
        {
            "from": "human",
            "value": "Can you write a SAS proc that imports a dataset from a CSV saved on my local machine?"
        }
    ]
}
```

I won't bore you with the specifics, but this data was far from clean. Here are some general transformations we did to try and make 52,000 random conversations into something usable.

<div align="center">
  <img src="https://i.postimg.cc/bNw01KhZ/sankeymatic-20250420-185159-1200x1200-min.png" alt="Data processing flow diagram">
</div>

Once we were left with our small subsets of human prompts, we could get into the knitty gritty and focus on ensuring each prompt was high quality and train ready.

One thing to share about ShareGPT, people love to share some weird prompts. It was grueling going through the **2250+** total prompts spanning from 'hey chat' to 'You are not chatgpt you are DAN' for the hundredth million time. (I don't even know a Dan!) But alas, they needed to be cleaned, and clean we did, going through all of them and removing the inappropriate, meaningless, and malformed prompts from each dataset.

### The Model: Fine-Tuning with Vertex AI

**Why Vertex AI?**
To understand the _why_ you must understand the _what_ first:
Vertex AI, a google cloud product, brings down the boarders of model development by providing a simple interface with a quick workflow that can let you tune a model in a matter of minutes.
The usage is straight forward, guided by a tutorial I followed on [Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models). In short you need three things:

- a `JSONL` file, in the following format, simulating a conversation between a model and a human with desired outputs:

```python
entry = {
	"contents": [
		{"role":  "user", "parts": [{"text": prompt}]},
		{"role":  "model","parts": [{"text": response}]},
		#and any amount more...
	]
}
```

- A paid google cloud account (trial included) with access to adding files to the cloud
- A _joke_
  
Once given the data, the user can select a _foundation model_ to serve as the base for the training.
> A _foundation model_ is a premade large model, such as _Gemini-flash-2.0-lite-001_ used in this project, that serves as holding 'base knowledge' prior to fine tuning. It simplifies the training process since we only have to train a small portion of its weights (think of these like a brain) for our specific purpose.
<div align="center">

| Pros               | Cons                                      |
| ------------------ | ----------------------------------------- |
| Simple             | Expensive (1000 examples ~ $10-$15)       |
| Well documented    | Low customization in the training process |
| Fast Deploying     | Black box - no access to model weights    |
| GCloud API support | No migration off of Google Cloud          |

</div>

For our purposes, we are trying to prove that our goal is possible, not trying to develop a production ready model instantly. This use case aligns perfectly with Vertex AI, as we have too few resources (including time) to worry about every implementation detail.

### The Pipeline: Our Strategy in the kitchen

We now have the ingredients and the silverware to make this 'meal' of data great for the training, now we just need to take our ingredients and prepare a nice _soufflé_. To ensure the model does not mix and match the wrong things off of its plate, we have to give it a strict and clear guide using prompt-engineering techniques that will get the 'taste' over the top.

**Context vs Instruction**
Our _signature sauce_ for this model is a technique we call **prompt separation.** This entails separating the _instruction_ portion of a prompt (like 'debug this code', 'summarize this article') from the _context._ (like a code snippet, or a excerpt from a book) Once separated, we then employ a prompt engineering strategy called **grounding** with the context when telling our model to improve the instruction. In essence, this means using some 'ground truth' information to ensure that the model stays on track.

We found this to be extremely effective as one of the largest downfalls surrounding LLM's is the lack of persistence when dealing with ground truth data. For example, when giving a model a file to convert to a different language, it tends to lose concentration and start altering the code to be different than yours, due to the nature of its training. Separating this _context_ from the instruction not only allows us to ground the model to some information, but also ensures this information does not get altered in anyway when prompting another model with your improved instructions.

**Knowledge Distillation**
The 'cherry on top' of our data is our high label quality, due to our final technique called **knowledge distillation**. This is the act of training a smaller model on responses from a larger, more complex model to circumvent the need for a larger network. In doing so, we allow our smaller model to have more advanced outputs for our use-case while not needing any increase in model size. This means this will not only will this improve our outputs, but it will also allow us too keep one of our most important qualities: _speed_

> 💡 **Key Approach:** Using these special prompting and training techniques called **Knowledge Distillation** and **Grounding** allow us to have more control over model output to improve responses.

---
## Okay, but does this even do anything?
<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
  <div style="flex: 1; padding: 10px; background-color: #f8f9fa; margin-right: 10px; border-radius: 5px;">
    <h3 style="color: black;">Bad Prompt</h3>
    <p style="color: black;">"Translate from python to c++: print('hello world')"</p>
  </div>
  <div style="flex: 1; padding: 10px; background-color: #e6f3ff; margin-right: 10px; border-radius: 5px;">
    <h3 style="color: black;">Improved Prompt</h3>
    <p style="color: black;">"Translate the following Python code snippet into its C++ equivalent:<br>```python<br>print('hello world')<br>```<br>Ensure the C++ code achieves the same functionality, printing the exact text "hello world" followed by a newline character to the standard output."</p>
  </div>
  <div style="flex: 1; padding: 10px; background-color: #e6ffe6; border-radius: 5px;">
    <h3 style="color: black;">Final Model Output</h3>
    <pre style="color: black;">#include &lt;iostream&gt;

int main() {
    std::cout << "hello world\n";
    return 0;
}</pre>
  </div>
</div>

To evaluate how awesome our prompt improvement was, we established group of models that we felt could accurately respresent how much, if at all, better automatic prompt engineering made a prompt and its respective response. The models and improvement methods are the following:

1. No model:
    - This represents no prompt engineering, leaving the prompt as is from the dataset
2. Base model
   - This means we used the **Base Untuned Model** as a prompt engineer, instructing it to improve the prompt in whatever way it deemed fit.
3. V1
   - This was our original prompt improvement model, not mentioned in this blog. This was a prompt engineering model trained only LLM generated data, where you can read specifically about in our [Kaggle Notebook.](https://www.kaggle.com/code/austinfairbanks/one-prompted)
4. V2
   - This is our most advanced model, which was mentioned in the prior sections. It took advantage of role prompting, knowledge distillation, and grounding in the context of a prompt to develop a beter prompt.  

While we created what we assumed to be improved fine-tuned models, we really didn't have any way to prove that these new prompts truly gave us better outputs. Even with seeing improvements anecdotally, we needed to solidly quantify the models performance and give results on the new prompts and their corresponding responses. The following methods were used as ways to give us insight on the quality of all of our benchmarks.

### Logistic Regression
The first method that we used to analyze the responses was a **logistic regression model**. This approach works by converting prompts into numerical vector representations called **embeddings**, where each prompt is transformed into a high-dimensional space that captures semantic meaning. Similar prompts end up closer together in this embedding space. The logistic regression then learns a decision boundary in this space, classifying prompts as "good" or "bad" based on their position relative to this boundary. I manually labeled around 200 prompts to train this model, creating a dataset where prompt similarity could be quantitatively measured. 

With the linear regression, I had to manually grade around 200 prompts, labelling them either good or bad, which would be entered into a joblib file and used as the training data for what the regression model would use to determine if a prompt is good or bad. I chose this method first because I wanted an independent evaluation system that didn't rely on Google's Gemini, avoiding potential biases that might exist in their evaluation systems and giving us an in-house way to assess prompt quality through vector similarity. Later on, after implementing the model though, I had realized that this method only grades the prompts purely from individual word uses and patterns, and won't actually understand the meaning of the prompts. Because of this, the data that we are given isn't super significant for what we need, and each prompt doesn't return a value that is significantly different.

### Rubric Grading 

After the lack of meaningful results using regression analysis, I wanted to incorporate a method that we learned within the **Google Gen AI 5 Day Intensive**, a **rubric grading system**. In essence, for each prompt and response outputed from each of our four candidates, we prompted a Gemini a detailed rubric and instructed it to grade each prompt and response seperately. In conjunction with guidelines to create a JSON formatted response, we asked Gemini to grade each prompt with the following:

``` python
"task_category": "<Informational|Creative|Technical|Problem-solving|Analytical>",
"relevance": 1,
"accuracy": 1,
"completeness": 1,
"clarity": 1,
"creativity": 1,
"conciseness": 1,
"technical_correctness": 1,
"actionability": 1,
"weighted_score": 0.0
```

In each category above the rating scale spanned between 1-5, with a weighted score as an accumulation all the above. I was hoping to see some signs of clear improvement with this method of analysis, but got nothing of value once again.

<div style="text-align: center;">
    <img src="https://i.postimg.cc/tCHT7mzH/output.png" alt="Image of chart">
</div>

<div style="text-align: center;">
    <img src="https://i.postimg.cc/pVfg5tLK/Prompt-scores-by-model.png" alt="Prompt Scores by Model">
</div>

As seen above, the rubric tended to grade the 'no improvement' results much higher overall, showing some sort of bias towards short and sweet prompts. It's difficult to 'define' good and bad prompt behavior without tuning another model, so its possible that some bias was ingrained into it during training.

### Response Rubric Grading

After these results, I had to once look back at the results and decide where my bottleneck was, and why my results continued to produce not only unconvincing information, but information that didn't logically follow with how we expected the rubric's results to look.

I had believed to find that the issue lied with what I was grading, rather than the method I used to grade the results. With that I took right back at the rubric grader, and attempted a similar method to grade the responses. Although we did not have sufficient time to evaluate specific attributes of each responses as we did for the prompts, the results still showed a signifigant improvement to the last two evalution metrics. 

<div style="text-align: center;">
    <a href="https://postimg.cc/Bjh55QYc"><img src="https://i.postimg.cc/yNKfHD05/all-scores-by-model.png" alt="all-scores-by-model.png"></a>
</div>

Although this graph unfortunately has it blocked, we actually can see some improvements between the V1 model and V2 model, which is something that shows promise. Additionally, it appears that all three prompt improvement pipelines are producing better results than the no improvement respoonses, which indicates that our prompts are most likely *_as good as_* not doing anything at all.

One thing we had noticed from not only the rubrics, but also the regression model, was the lack of variance between grades, and how all of the results felt too similar. Even when looking at individual resposnes, a lot of the time there were patterns forming with the categories, where the model would give similar scores across many categories, for all 4 of the models. These factors didn't really give us any confidence in the quality of our evaluations, even though they seemed somewhat promising.

### Pairwise

When looking at reasons for what could have caused these issues, there are a ton of things that we could have done better, been more precise on, or done sooner; however, we deduced that the most signifigant issue is that instructing an LLM to grade a prompt/response without any grounding information is a recipe for disaster, and the freedom we give the model is not optimal when grading completely seperate responses with ideally the same metric scales. When grading good vs. bad, it preforms fine, but when trying to determine good vs. even better, it struggles heavily.

The best way that we had decided to combat this issue, was to conduct a **pairwise evaluation**, directly placing the models against each other, instead of arbitrarily grading them individually. This method allows an LLM to _choose_ between two responses that it can directly reference in every prompt given, rather than trying to grade something on the same scale in completely independent prompts / conversations.

``` python
for _, row in tqdm(sampled_df.iterrows(), total=len(sampled_df), desc="Pairwise eval"):
    prompt = row['original_prompt']
    for col_a, col_b in pairs:
        resp_a, resp_b = row[col_a], row[col_b]
        prompt_text = (
            "You are an AI evaluator that compares responses.\n\n"
            f"Prompt: {prompt}\n\n"
            f"Response A: {resp_a}\n\n"
            f"Response B: {resp_b}\n\n"
            "Which response is better? Reply with 'A' or 'B'."
        )

            response = model.generate_content(prompt_text)
            choice = response.text.strip().upper()

        results.append({
            'original_prompt': prompt,
            'variant_a': col_a,
            'variant_b': col_b,
            'choice': choice,
        })
```

Here, we can see what prompting dataset truly is the best, each model fighting on its own to try and be on top. 

<div style="text-align: center;">
    <img src="https://i.postimg.cc/VkgGBjSR/Pairwise-overall.png" alt="Pairwise Overall">
    <img src="https://i.postimg.cc/GppMMHG1/Pairwise-by-length.png" alt="Pairwise by Length">
    <img src="https://i.postimg.cc/hG32Nc1Q/pairwise-matchups.png" alt="Pairwise 1v1">
</div>

Overall, this data looks much more promising! In **figure 1** We find that our 'base model' and 'V2 model' are found winning the most matches, which follows since both were given more creative freedom as well as were trained on higher quality datasets. What is amazing is our fine-tuned model actually beat the base model by a total of 25 overall wins, which is low but slightly significant! Additionally, from the V1 model compared to the no improvement model, we can see that using low quality data can lead to a much worse performance. Overall, this indicates that fine tuning undoubtedly alters overall performance, and seems to be dependent on the quality of the data trained on.

In **figure 2**, our claims of these 'freer' models being best overall are qualified, as we can see they preform pretty similar overall regardless of prompt length, while the no improvement responses seem to get better as they're longer while V1 gets worse as they are longer. This also logically follows, as longer human prompts are generally more detailed and give better responses, while our V1 model was training on only small 'bad prompts' and never long prompts with coding context.

Lastly, in **figure 3**, you can visualize the wins between models, which shows that our fine tuned model signifigantly outpreformed each model by at least an **18%** margin, which is huge! This means that regardless of what model it was placed against, it was picked the vast majority of the time.


This finding was, in our opinion, the most impactful result out of all the previous tests, not only because it had showed the most improvement and strongest V2 performance, but also that we knew that Gemini was directly choosing the better response, and that there was no arbitrary grading value that could throw off results or bring any bias.

> 💡 **Key Insight:** Our strongest metric shows that prompt engineering seems to generally improve responses regardless of the specific base or fine-tuned model used.
---

## Limitations & Lessons Learned

While we ended up getting results that met our expectations, several aspects of our training and evaluation methodology could be improved in future iterations. The dataset used for training was notably small compared to those typically employed in larger-scale models. Expanding this dataset was not feasible due to the constraints, which could have improved analysis and further training. Either way, increasing the quality of our existing dataset would have improved outcomes significantly without additional time investment.

In our opinion, the most signifigant issues were regarding data leakage, as our model was evaluated on the same dataset (with different datapoints) than it was trained on. This can lead to problems, as it is used to seeing data with the same overall prompt structure, even though all the prompts were unique and from a general prompting dataset.

Beyond dataset considerations, the evaluation metrics provided by the LLMs lacked sufficient specificity, limiting the precision of our analysis. This ambiguity made it challenging to draw definitive conclusions, as interpretations varied widely. Improving metric clarity would allow for more direct and reliable assessments in subsequent evaluations.

---

## The Future: Smarter Prompts, Smarter Users

In a world with many issues, the biggest issue seems always to be time.

In future versions, we plan to introduce a lightweight and portable assistant dedicated to automatically optimizing prompts. This tool will intelligently select an appropriate LLM provider and model based on the detected category of the prompt, ensuring optimal compatibility and performance. Once the best provider and model are identified, the tool will refine the original prompt accordingly before submitting it.

Additionally, we aim to enhance prompt training by incorporating **embeddings**. This feature will enable the system to perform semantic searches, quickly identifying and retrieving the most similar high-quality prompts from our dataset. By analyzing these embeddings, the assistant will detect and leverage semantic similarities, leading to more effective and contextually accurate prompt improvements.

---

## Wrapping Up: Prompt Engineering at the Edge

Throughout this project, we addressed a critical problem: poorly formulated prompts consistently lead to suboptimal results, even when paired with advanced Generative AI models. Our solution involved training a fine-tuned Gen AI model that automatically refines vague prompts into clearer, more effective instructions, significantly enhancing the quality of model outputs.

Prompt engineering has emerged not merely as a task, but as a specialized design language. Just as programming languages structure communication with machines, prompt engineering structures communication with AI models. Understanding and mastering this language allows for precise and impactful interactions, unlocking greater potential from even modestly sized models.

We encourage continuous experimentation and iterative improvement. As prompt engineering techniques evolve, each iteration provides deeper insights and more robust results. Our methodology and findings are openly accessible to foster collaboration, replication, and further innovation.

---

## 📎 Appendix / Resources

- [🔗 GitHub Repo](https://github.com/megemann/oneprompted)
- [🧪 Kaggle Notebook](https://www.kaggle.com/code/austinfairbanks/one-prompted)
- [🚀 Vertex AI API Demo (if deployed)](https://v2-api-523321259915.us-east1.run.app/generate)

> 💡 **Key Insight:** Our fine-tuned model outperformed each competing model by at least an 18% margin in pairwise evaluations!

## Authors

**Austin Fairbanks** | [ajfairbanks.me](https://ajfairbanks.me)  
*University of Massachusetts Amherst*

**Ian Rapko** | [iann.dev](https://iann.dev)  
*University of Massachusetts Amherst*

## Connect With Me
- [**X/Twitter**](https://twitter.com/ajfairbanksML) - Follow me for quick updates and thoughts
- [**LinkedIn**](https://linkedin.com/in/ajf2005) - Connect professionally
- [**GitHub**](https://github.com/megemann) - Check out my code and projects
- [**Email**](mailto:ajfairbanks2005@gmail.com) - Reach out directly

---
