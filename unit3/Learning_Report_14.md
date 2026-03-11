# Deep Research

## Burnout

The first task that I tackled with a mult agent workflow was configuring and using the Deep Research Workflow that was given in the Lecture Notes. I found it easy to set up.

Most interestingly with this workflow was the clarifying questions Agent, or Topic Expander. I have used LLMs before to help clarify my thinking or ideas about a topic before and found it one of the best uses for single shot LLM prompts. Just having it ask questions in response to my prompt and trying to understand what I was after was useful for me to think about what it was that I wanted to understand.

## Sugar

I wanted to learn more about how sugar impacts metabolism and the Deep Research Workflow interpreted my request as if I were trying to conduct research on myself. This just goes to show that the topic expander Agent in deep_research.yaml file was really focused on the research aspect of its role, even to the point that it thought I was going to conduct research instead of asking it to conduct research. Makes me wonder how this could be improved.

# Creating an Agent Workflow: Website Developer

I have included the frontend_prototyper.yaml which describes the three agents that I used in this workflow: Designer, Architect, and Builder. I decided to streamline the conversation with the user with stdout statements instead of piping it through an LLM. If there were a need for translation or other more complicated input proccessing, I would have included a chat LLM.

This Agent Workflow worked pretty well, except that the builder agents were not able to sync with each other to accomplish necessary tasks. I found that the type definitions for one file did not necessarily match another and so the resulting code is pretty sloppy and error prone. But, and this is an important but, it does output code into the desgnated files and they function as a typescript project.

If I had more time I would go back and ensure that it does not output any emojis, which seemed to cause issues with my terminal when displaying output, and iron out any remaining remaining kinks in the workflow. I might include an orchestrator to help ensure that the builders code work together in some way.

# Reviewing shared videos & sharing videos

I watched two Ted talks about AI and reasoning:

- Is AI making us dumber? Maybe
- How to stop AI from killing your critical thinking

Both were very good and speak to the use of AI as tool to facilitate and augment thought, not replace it entirely.
    