# Brain storming ideas

- Curated reading lists
- Recipe creator
- Study assitant/Learning tool
  - Ingest reading assignment
  - Interact with text with a user per https://www.youtube.com/watch?v=3lPnN8omdPA

# Did some research on Studying tools

notebooklm.google.com
studley.ai
turbo.ai

It seems like most of them are designed to make the studying process easier and more engaging. While those are not bad things per se, I want to make a tool that helps users interface with the material more direclty. A tool that makes a user think and doesn't just automate a task or speed up cognitive labor. I would love to actually help users slow down and think about a process beyond their initial thoughts.


# Discussion re: Cognition with Claude

I had a little chat with Claude about things that could improve cognition and some of the challenges of retaining users when using what claude called fricton by design.

## Ideas it came up with that I liked
It came up with several, but I settled on these three because they were similar to ideas that I had had in the past. 

1. Argument Mapping/Fallacy checker/Logic improver
2. Focus training
3. Idea Consolidation/Revisitng ideas like Anki, but not just for flashcards


# Argument Mapping 

After discussing possibilities and pheasibility with Claude for over an hour, I settled on Argument Mapping, although I may call it something better. 

It is more like a belief/argument deepener, it is designed to push the user to establish their premises, articulate their beliefs, and improve their reasoning abilities over time. So its less of an argument mapper than it is a tool to improve the user's reasoning. At least, thats my goal.

# Main Agent

I've worked on an initial draft of the main agent that will be chatting with the user. I think I'll also use a second agent to be used as a tool for the main agent to identify flaws in logic, provide counter arguments, and other confrontational ideas. This should help isolate the main agents concerns to focus more wholy on improving the users argument. 

In a couple tests that I did with this is becomes apparent that prompt engineering will be a significant challenge for this projec as getting the tone right will be tricky. I also want to improve the user interface so that the user doesn't have to type everything in every single time, they should be able to start with what they already have. 

## 