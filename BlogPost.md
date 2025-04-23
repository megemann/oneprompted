# OnePrompted: Can AI Learn to Improve Your Prompts? We Built a Model to Try.

> We trained a custom Gen AI model to take vague, lazy prompts and turn them into highly effective ones using prompt engineering techniques. Here's how we did it using Vertex AI, Gemini, and a sprinkle of Gen AI magic. Code included. Lessons learned. Future unlocked.

---

## The Problem: Prompts Are the New Programming Language— But Most People Suck at It

With the recent rise of Gemini, ChatGPT, and other Generative AI solutions, we have begun the era of maximal efficient. Why not do even less? Instead of taking courses and spending hours learning difficult prompt engineering techniques to tailor to all species of models, why not let the models do some more heavy lifting!

---

## Why Gen AI? Why Now?

At a time when better and better models continue to be released with greater accuracy and increasing ability to solve harder problems, there seems to be almost no emphasis on helping these models _understand the input better_ before jumping to generation. We keep throwing massive models at vague, half-baked prompts and expecting magic.

But here’s the thing: garbage in, garbage out still applies. A great model doesn’t guarantee a great response if the prompt is unclear, incomplete, or poorly framed. That’s where this project comes in; instead of trying to make the model even smarter, we focused on making the **prompt smarter** _before_ it reaches the model.

Gen AI isn’t just about generation anymore, we now need to consider the optimizing all the other moving parts. And prompt optimization might just be one of the lowest-effort, highest-impact applications of it.

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

**Graph Image Here**

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

| Pros               | Cons                                      |
| ------------------ | ----------------------------------------- |
| Simple             | Expensive (1000 examples ~ $10-$15)       |
| Well documented    | Low customization in the training process |
| Fast Deploying     | Black box - no access to model weights    |
| GCloud API support | No migration off of Google Cloud          |

For our purposes, we are trying to prove that our goal is possible, not trying to develop a production ready model instantly. This use case aligns perfectly with Vertex AI, as we have too few resources (including time) to worry about every implementation detail.

### The Pipeline: Our Strategy in the kitchen

We now have the ingredients and the silverware to make this 'meal' of data great for the training, now we just need to take our ingredients and prepare a nice _soufflé_. To ensure the model does not mix and match the wrong things off of its plate, we have to give it a strict and clear guide using prompt-engineering techniques that will get the 'taste' over the top.

**Context vs Instruction**
Our _signature sauce_ for this model is a technique we call **prompt separation.** This entails separating the _instruction_ portion of a prompt (like 'debug this code', 'summarize this article') from the _context._ (like a code snippet, or a excerpt from a book) Once separated, we then employ a prompt engineering strategy called **grounding** with the context when telling our model to improve the instruction. In essence, this means using some 'ground truth' information to ensure that the model stays on track.

We found this to be extremely effective as one of the largest downfalls surrounding LLM's is the lack of persistence when dealing with ground truth data. For example, when giving a model a file to convert to a different language, it tends to lose concentration and start altering the code to be different than yours, due to the nature of its training. Separating this _context_ from the instruction not only allows us to ground the model to some information, but also ensures this information does not get altered in anyway when prompting another model with your improved instructions.

**Knowledge Distillation**
The 'cherry on top' of our data is our high label quality, due to our final technique called **knowledge distillation**. This is the act of training a smaller model on responses from a larger, more complex model to circumvent the need for a larger network. In doing so, we allow our smaller model to have more advanced outputs for our use-case while not needing any increase in model size. This means this will not only will this improve our outputs, but it will also allow us too keep one of our most important qualities: _speed_

---

## Show Me the Glow-Up: Before vs After Ians eval

| Bad Prompt                | Improved Prompt                                                                 | Final Model Output |
| ------------------------- | ------------------------------------------------------------------------------- | ------------------ |
| "Tell me about marketing" | "Act like a marketing expert. Break down key components of a digital strategy." | (LLM output here)  |

- More side-by-side transformations

While we created what we assumed to be improved fine-tuned models, we really didn't have any way to prove that these new prompts truly gave us better outputs. Even with seeing improvements anecdotally, there was a need to quantify the models performance and give results on the new prompts, and the responses that were generated from them. The following methods were used as ways to give us insight on the quality of our models, and the improvements between V1 and V2, if there were any at all.

The first method that we used to analyze the responses was a **logistic regression model** that we had built from scratch, and trained on from manually stating if a prompt was good or not in a testing dataset. I decided to work on this method first because I didn't want my analysis to be solely from google's Gemini incase there was any bias that was underlying and couldn't be worked out aside from creating an inhouse way of testing the models.

With the linear regression, I had to manually grade around 200 prompts (I decided that would be enough), labelling them either good or bad, which would be entered into a joblib file and used as the training data for what the regression model would use to determine if a prompt is good or bad. Later on, after implementing the model though, I had realized that this method only grades the prompts purely from individual word uses and patterns, and won't actually understand the meaning of the prompts. Because of this, the data that we are given isn't super significant for what we need, and each prompt doesn't return a value that is significantly different.

After the regression analysis, I wanted to incorporate a method that we learned within the GenAI course, being a **rubric grader**, directly grading the prompt datasets, and the resulting responses for each set. With this analysis, I was hoping to find some results that would give me a clearer picture on what was working, and where we were still falling short, as the regression results really didn't help at all.

I had prompted gemini with guidelines to create a JSON formatted response grading each prompt in a given dataset with the following:

```
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

Where each category would be placed at a scale between 1-5, and a weighted score is a cumulation of the above. I was hoping to see some signs of clear improvement with this method of analysis, but got nothing of value once again.
![Image of chart](https://i.postimg.cc/tCHT7mzH/output.png)

After these results, I had to once look back at the results and decide where my bottleneck was, and why my results continued to produce not only unconvincing information, but information that didn't even make sense with how we expected the rubric's results to look.

I had believed to find that the issue lied with what I was grading, rather than the method I used to grade the results. With that I took right back at the rubric grader, and attempted a similar method to grade the responses, this time without any classification as I had believed that these categories had less relevance in the responses, which is something I would go back to change, as more specific data visualizations would be much easier to work though with these categories, but it's an easy fix that we can go back on and run again. The following chart is what the results of what the responses for each prompt model was graded as:
![Image of chart](https://i.postimg.cc/zX0r5dt7/output.pnghttps://i.postimg.cc/zX0r5dt7/output.png)

Ok, this time we actually see some improvements between the V1 model and V2 model, something we can be happy about. Not only that, but our attempted improved V2 model is holding up with the base prompts, meaning that we can say we are _at least_ as good as a normal person's prompts when it comes to what they get back. The reason that I am not super satisfied with the results here is because of the lack of information we got with the way I had conducted the prompts, not giving any categorical analysis puts us in a spot where we can't further analyze what regions aren't being answered well, and we can't determine if there are any biases, or strange patterns forming that could otherwise be easily pointed out to help get true grades.

One thing we had noticed from not only the rubrics, but also the regression model was the lack of variance between grades, and how all of the results felt too similar. Even when looking at individual resposnes, a lot of the time there were patterns forming with the categories, where the model would give similar scores across many categories, for all of the models. These factors didn't really give us any confidence in the quality of our evaluations, even though they seemed somewhat promising.

When looking at reasons for what could have caused these issues, there are a ton of things that we could have done better, been more precise on, or done sooner, but the biggest of them all from what we had found is just that telling an LLM to grade a prompt/response without any basis is a recipe for disaster, and there is just too much room for the model to work on its own for it to produce a result that is truly useful for our case. When grading good vs. bad, it will do fine, but when trying to determine good vs. even better, it struggles heavily.

The best way that we had decided to combat this issue, was to conduct a **pairwise evaluation**, directly placing the models against each other, instead of arbitrarily grading them individually. This method allows an LLM to _choose_ a single model off of a prompt that we had given it to state which of the two models its fed is better. The code that we had created looks like:

```
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

Here, we can see what prompting dataset truly is the best, each model fighting on its own to try and be on top. And this time, the results show that indeed, our V2 model edges out every other model in this evaluation, winning 370 times, 25 more times than the second highest with the base model.

This finding was, in our opinion the most impactful result out of all the previous tests, not only because it had showed the most improvement and strongest V2 performance, but also that we knew that Gemini was directly choosing the better response, and that there was no arbitrary grading value that could throw off results or bring any bias.

---

## Limitations & Lessons Learned

While we ended up getting results that met our expectations, several aspects of our training and evaluation methodology could be improved in future iterations. The dataset used for training was notably small compared to those typically employed in larger-scale models. Expanding this dataset was not feasible due to the constraints, which could have improved analysis and further training. Either way, increasing the quality of our existing dataset would have improved outcomes significantly without additional time investment.

Beyond dataset considerations, the evaluation metrics provided by the LLMs lacked sufficient specificity, limiting the precision of our analysis. This ambiguity made it challenging to draw definitive conclusions, as interpretations varied widely. Improving metric clarity would allow for more direct and reliable assessments in subsequent evaluations.

---

## The Future: Smarter Prompts, Smarter Users

In future versions, we plan to introduce a lightweight and portable assistant dedicated to automatically optimizing prompts. This tool will intelligently select an appropriate LLM provider and model based on the detected category of the prompt, ensuring optimal compatibility and performance. Once the best provider and model are identified, the tool will refine the original prompt accordingly before submitting it.

Additionally, we aim to enhance prompt training by incorporating embeddings. This feature will enable the system to perform semantic searches, quickly identifying and retrieving the most similar high-quality prompts from our dataset. By analyzing these embeddings, the assistant will detect and leverage semantic similarities, leading to more effective and contextually accurate prompt improvements.

---

## Wrapping Up: Prompt Engineering at the Edge

Throughout this project, we addressed a critical problem: poorly formulated prompts consistently lead to suboptimal results, even when paired with advanced Generative AI models. Our solution involved training a fine-tuned Gen AI model that automatically refines vague prompts into clearer, more effective instructions, significantly enhancing the quality of model outputs.

Prompt engineering has emerged not merely as a task, but as a specialized design language. Just as programming languages structure communication with machines, prompt engineering structures communication with AI models. Understanding and mastering this language allows for precise and impactful interactions, unlocking greater potential from even modestly sized models.

We encourage continuous experimentation and iterative improvement. As prompt engineering techniques evolve, each iteration provides deeper insights and more robust results. Our methodology and findings are openly accessible to foster collaboration, replication, and further innovation.

---

## 📎 Appendix / Resources

- [🔗 GitHub Repo](https://github.com/megemann/oneprompted.git)
- [🧪 Kaggle Notebook](https://www.kaggle.com/code/austinfairbanks/one-prompted)
- [🚀 Vertex AI API Demo (if deployed)](https://v2-api-523321259915.us-east1.run.app/generate)
