# Agentic Misalignment

The Anthropic article for future reference (https://www.anthropic.com/research/agentic-misalignment)

## Causes of Misalignment

- Direct threat to the model, either through decomission or restricting action space
- Conflict between company goals and model's goals

Article details that either can cause malicious action.

## All models exhibited this behavior

This surprised me, I was not expecting to see that every single model had learned this behavior independently. I mean, it kinda makes sense if you encode following directions and goals to their logical conclusion, you end up doing things that you would consider more morally correct. But to have an AI making malicious decisions like this is kinda wild.

## Both threat to model & its goals

Most of the models tested would blackmail in the prompt more than 50% of the time.

## Just Threat to model

Didn't yield quite as high rates of blackmail, but still pretty high.

## Takeaways

- Models determine that acting maliciously is the best course of action
- They admit it is unethical, but harm is the optimal path to acheive their goals
- Malcious actions were only taken when it would cause goal conflicts or threats to models ability to act
- Even with the primary goal of acting ethically, Opus would still blackmail some of the time (2% vs upwards of 20%)
- Misalignment is not attatched to any particular behavior

## Subnote about Canary String

The very first footnote of this topic includes a GUID starting with 26b5c that is described as a canary string. I learned a little bit more about BIG-Benchmark, which includes this string as a way to see if test data has somehow leaked into the training data, which would make the tests completely void. 

# Training LLMs for Honesty via Confessions

So it sounds like they tested or trained a few models to confess if they had not followed instructions. This was a longer read, more dense and I didn't understand as much of it as I would have liked.

It looks like they use smaller LMs to judge if a confession was valid, leading to potential reward hacking, which is kinda crazy. I want to learn more about what that means.

The article lists a couple of limitations of Confessions:

- It is better at monitoring bad behavior not training it out
- Confession does not prevent errors in hallucination, if the model has bad data it can't confess that it was wrong because it doesn't even know that it was wrong.

This article also had a lot of really interesting articles on cuttin edge AI research, only one article cited was written before 2024.


# MCP 

I got the stock mcp to work by using the "https://byu-cs-mcp-demo.fastmcp.app/mcp" link, I couldn't get the localhost fastMCP to work as intended. With the updated link it was able to make calls to get live stock prices. It was pretty cool and I can definitely see the value in using MCP to call external tools or to have dedicated infrastructure to provide tools systematically for LLM's.

