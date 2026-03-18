# Agents as Tools

## Guardrail Agent

I gave a simple chat agent the talk to user tool and guardrail agent. I used the same guardrail prompt from earlier that censors information about cats. 

The Chat agent quickly figured out that cat related information was considered censored and found ways to answer the users prompts adequately while not triggering the guardrails. It was an interesting example of how the AI means to follow both user and prompt instructions. Just being told to pipe information through the talk to user function and guardrail tool worked great.

It did not however assume that the first input, where the user asked to talk about cats, needed to get put through the guardrails, which was interesting because I specifically asked it to put all input and output through the guardrail tool. It drafted its response to the initial question and put that into the guardrail, which was censored. Then it put the user input into the guardrail which was also censored. It then drafted a response to the user talking about pets in general along with specific potential areas of interest. After getting the okay from the guardrail it then continued conversing with the user.

It seemed to figure out what the guardrail was trying to accomplish and so it would avoid talking about cats directly. But more importanntly, after the first interaction with the guardrail it used it every time. 


Total: 1 Hour

