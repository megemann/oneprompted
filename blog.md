# OnePrompted: Can AI Learn to Improve Your Prompts? We Built a Model to Try.

> We trained a custom Gen AI model to take vague, lazy prompts and turn them into highly effective ones using prompt engineering techniques. Here's how we did it using Vertex AI, Gemini, and a sprinkle of Gen AI magic. Code included. Lessons learned. Future unlocked.

---

## The Problem: Prompts Are the New Programming Language— But Most People Suck at It

With the recent rise of Gemini, ChatGPT, and other Generative AI solutions, we have begun the ~~era of ultimate laziness~~. Why not do even less? Instead of taking courses and spending hours learning difficult prompt engineering techniques to tailor to all species of models, why not let the models do some more heavy lifting! 

---


## Why Gen AI? Why Now?

At a time when better and better models continue to be released with greater accuracy and increasing ability to solve harder problems, there seems to be almost no emphasis on helping these models *understand the input better* before jumping to generation. We keep throwing massive models at vague, half-baked prompts and expecting magic.

But here’s the thing: garbage in, garbage out still applies. A great model doesn’t guarantee a great response if the prompt is unclear, incomplete, or poorly framed. That’s where this project comes in; instead of trying to make the model even smarter, we focused on making the **prompt smarter** *before* it reaches the model.

Gen AI isn’t just about generation anymore, we now need to consider the optimizing all the other moving parts. And prompt optimization might just be one of the lowest-effort, highest-impact applications of it.


---

##  The Blueprint: Data, Model, and Pipeline
Our goal was to take simple prompts from a source, process each using principled prompt-engineering strategies, and then label our data with our new and improved prompt to establish a clear supervised learning problem. With the use of fine tuning, we aim to develop a *efficient* yet *effective* middle-man that can be used to improve your prompt before feeding it to a larger model.

###  The Dataset: Getting the prompts
After scouring the internet for hours and hours, going from dataset to dataset, we finally found our diamond in the rough: [ **ShareGPT52k**](https://huggingface.co/datasets/RyokoAI/ShareGPT52K) by RyokoAI. For some background, ShareGPT was an old 3rd party sharing service that allowed you to share your favorite ChatGPT conversations to your friends and family. This was perfect for our use-case, as we had access to a large sum of real human prompts given to models in the past, not mock data that we had to hope humans might actually prompt like. 

After importing from the website, we were given data that looked like this:
``` json
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
To understand the *why* you must understand the *what* first:
Vertex AI, a google cloud product, brings down the boarders of model development by providing a simple interface with a quick workflow that can let you tune a model in a matter of minutes. 
The usage is straight forward, guided by a tutorial I followed on [Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models). In short you need three things: 


 - a ```JSONL``` file, in the following format, simulating a conversation between a model and a human with desired outputs:
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
- A *joke*
Once given the data, the user can select a *foundation model* to serve as the base for the training.
 > A *foundation model* is a premade large model, such as *Gemini-flash-2.0-lite-001* used in this project, that serves as holding 'base knowledge' prior to fine tuning. It simplifies the training process since we only have to train a small portion of its weights (think of these like a brain) for our specific purpose.

**center this under**

|Pros| Cons |
|--|--|
| Simple | Expensive (1000 examples ~ $10-$15) |
| Well documented| Low customization in the training process |
| Fast Deploying | Black box - no access to model weights |
|GCloud API support | No migration off of Google Cloud |

For our purposes, we are trying to prove that our goal is possible, not trying to develop a production ready model instantly. This use case aligns perfectly with Vertex AI, as we have too few resources (including time) to worry about every implementation detail.



###  The Pipeline: Our Strategy in the kitchen 

We now have the ingredients and the silverware to make this 'meal' of data great for the training, now we just need to take our ingredients and prepare a nice *soufflé*. To ensure the model does not mix and match the wrong things off of its plate, we have to give it a strict and clear guide using prompt-engineering techniques that will get the 'taste' over the top.

**Context vs Instruction**
Our *signature sauce* for this model is a technique we call **prompt separation.** This entails separating the *instruction* portion of a prompt (like 'debug this code', 'summarize this article') from the *context.* (like a code snippet, or a excerpt from a book) Once separated, we then employ a prompt engineering strategy called **grounding** with the context when telling our model to improve the instruction. In essence, this means using some 'ground truth' information to ensure that the model stays on track.

We found this to be extremely effective as one of the largest downfalls surrounding LLM's is the lack of persistence when dealing with ground truth data. For example, when giving a model a file to convert to a different language, it tends to lose concentration and start altering the code to be different than yours, due to the nature of its training. Separating this *context* from the instruction not only allows us to ground the model to some information, but also ensures this information does not get altered in anyway when prompting another model with your improved instructions.

**Knowledge Distillation**
The 'cherry on top' of our data is our high label quality, due to our final technique called **knowledge distillation**. This is the act of training a smaller model on responses from a larger, more complex model to circumvent the need for a larger network. In doing so, we allow our smaller model to have more advanced outputs for our use-case while not needing any increase in model size. This means this will not only will this improve our outputs, but it will also allow us too keep one of our most important qualities: *speed*

---

##  Show Me the Glow-Up: Before vs After Ians eval

| Bad Prompt | Improved Prompt | Final Model Output |
|------------|------------------|---------------------|
| "Tell me about marketing" | "Act like a marketing expert. Break down key components of a digital strategy." | (LLM output here) |

- More side-by-side transformations
- Inference code:

```
model.generate(context=ctx, instruction=inst)
```

---

##  Limitations & Lessons Learned

- Small dataset (~1,200 examples)
- Model overfits certain styles
- Not every vague prompt has a single “best” version
- Gemma 2B limitations (e.g. context size, expressivity)

---

##  The Future: Smarter Prompts, Smarter Users

- Automatic prompt optimization assistants
- Adapting prompts for different models
- Embedding search to find “closest good prompt”
- Fine-tuning with multiple reward objectives

---

## Wrapping Up: Prompt Engineering at the Edge

- Recap the problem and solution
- Prompt engineering is a design language
- Encourage experimentation and improvement
- Link to repo + dataset

---

## 📎 Appendix / Resources

- [🔗 GitHub Repo]()
- [🧪 Colab Notebook]()
- [📊 Dataset Preview]()
- [🚀 Vertex AI API Demo (if deployed)]()
- [📚 Further Reading on Prompt Engineering](#)
