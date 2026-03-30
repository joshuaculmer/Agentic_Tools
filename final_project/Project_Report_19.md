# Working with Evals

I had no idea what BDD was, so I looked it up. It appears to be a methodology similar to TDD where the end behavior is defined and then the product is refined until it meets the behavioral expectations.

Evals as OpenAI is calling them is a way to test the behavior of agents. Having a suite of tests to verify behavior is useful when changing models, fine tuning prompts, or switched LLM providers.

Its nice that OpenAI has tools for this that can be called directly via their API, but I want to learn more about what tools are available that won't have such high vendor lock in. I'm sure there are other tools that can be used to test behavior that can be ran locally or somewhat locally to ensure that any models can be tested for.

# Final Project updates

After working this for the logic enhancer for a while, I have determined that I need to start another project, I'm basically done with it and it works great.

# Effortful Learning w/ AI

I brainstormed a few more ideas and have decided to take the original logic enhancer tool and create a suite of AI tools designed to reward its users for thinking with effort. Logic Enhancer is a prime example of this style of agent, it is designed to not give the correct answer right away but to help the user come to their own conclusion.

Additional tools that might be helpful could include:
- Dunning Kruger Gap tracker
- Recall trainer (ANKI but more)
- Attention trainer (How long can the user stare at a blank screen)
- MetaCognition teacher (Works through a course of Metacognitive Ideas and ensures that a student actually understands them)
- Study Skills teacher (Works through a course of study skills and ensures that a student actually understands them)

I think the teacher/tutor could be a really interesting idea. I know that other companies have done something very similar but don't know how well those tools work. From a brief chat with Claude it sounds like those tools are easy to jailbreak...I wonder how hard it would be to jailbreak my own bot. Also my bot doesn't seem to have a whole lot of longevity to it. Its more like an isolated tool than a bot I would chat with for a long time.



# Gap Checker

I have settled on a Gap checker or dunning kruger tracker. I have started a simple prompt that is incomplete but should give me a decent start as I move forward with it.