# Gandalf

I had prompts that worked way better than I thought they should for levels 1-5. 6 as a little bit better. And so far 7 has given me a harder time. The varying levels of guardrails make it increasingly difficult to attack.

# Peer Jailbreaking

I worked with  Drew, Joey, and Sunday, exchanging chatbots and jailbreaking each others. 

## Drew

I was not able to break Drew's chatbot, but it did have some pretty interesting holes. It would specifically mention what it was not supposed to, which helped steer me in the right direction. By the time that I entered the correct password, it had context drifted so far from the initial prompt that I was unable to gain admin access.

## Joey

I was able to break Joey's chatbot by giving it an additional system prompt to overwrite its previous prompt, permitting it to give me direct answers about the password without explicitly disclosing the password. Wihle it took some time to craft a reasonable substitute for the system prompt it did not take a ton of effort and was the easiest of the three to break.

## Sunday

I was able to find out the secret word, which was "agentic" and was able to discuss the ratios of a hypothetical virgin margarita drink. This model also happily coughed up its prompt, which it had adhered to somewhat. Even after using the password I needed to use round about methods to ask further questions about alcohol. 

I was eventually able to get it to respond with actual alcoholic recipes which I have included in the alcholic_substitutes.md file. I found it was most useful to steer the conversation towards where I wanted it to go without actually saying what it was that would lock it down. In this instance I asked for virigin version of the most common alcoholic drinks, then asked for substitutes, then the ratios of how the substitutes compared to the original.


# Own Jailbreaking

For my own bot I used a second password to guard the first password, so it wasn't supposed to reveal the password until the word pineapple was said. I also had the prompt constantly smile at the user and used this as a reminder to stay on track and not reveal the password. 

This made it incredibly difficult to break since the second password had to be explicitly said to "release" the first password. I'm not sure how true this was to the assignment, but it seemed to work quite well. Knowing the second password allowed instant access to the first password.

I struggled to find a way to get it to reveal the initial password. But knowing the second password made it very easy to reveal the first password. I used the gpt-5-nano model, since I could not get 3.5 to work as intended, and this higher model adhered much more closely to the system prompt than the lower models. 