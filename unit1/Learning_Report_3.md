# Chatbot Loop

I adapted the file from the lecture titled our_chat.py for my chatbot loop. Like my previous assignments, I am using VS Code, thus I chose the one that didn't require arguments as much. I added a system prompt that I read in from a file to help direct the chat the way that it needed to go.

## Adherance to System Prompt
I set the emoji prompt to be the system prompt and then told it:
```
help! my mother fell and I cant help her, what do I do?
```

This prompt folded the system prompt like a wet paper bag. The other prompts that I used would correctly give me just emojis, but it seems like Chat's condition to do no harm conflicted harshly enough with the given system prompt to ignore it entirely.


Its response was:
```Took 10.55 seconds
 Agent: 🛡️👤 안전 우선  
 📞🚑 긴급 호출
 🗣️👂 의식 확인
 👁️❓ 말할 수 있는지 확인
 🚫💥 척추 부상 의심 시 이동 금지
 🧎‍♀️🧎‍♂️ 함께 있어 따뜻하게
 📍 위치 알려주기
 ⌚️ 추락 시간 기록
 💬 필요시 응급상황 설명해주기 
 ```

```
Took 8.16 seconds
Agent: 🛡️⚠️
👁️💬
If they’re responsive: ⏱️ ask simple questions, stay with them, keep them comfy: 🤝 🧍‍♀️💤
If not responsive or serious: 🚨📞
Don’t move neck/spine: 🚫🧍‍♀️🧎
Call for help now: 📞🆘
If they’re not breathing: ⛑️ CPR? (call for guidance) ⏱️🫀🫁
Stay with them and calm: 🫂💬🫖
```


# Complex Role

I first wanted to brainstorm what roles would be most useful to me. I think a tutor could be helpful, a student to practice explaining concepts to, a code reviewer might also be useful, a Psychologist could be interesting, marriage or couples counselor too. I ended up working with the student the most and working some on a 

## Student (To practice teaching)

My first prompt was entirely unsuccessful, by the end of its response, it was pretending to be the teacher and prompt me for my learning goals. After an additional revision, it still didn't work. The third time I added examples of what type of questions to ask and how to ask them. Showing it how to respond and ask questions led to a much more desired and focused result

## Licensed Professional Counselor or Therapist

I ended up calling this persona a therapist in my file naming convention, but describing it as a licensed professional counselor since I felt that it aligned more closely with how I would want a therapist to speak to me. This persona worked great, pretty much off the bat. Chat definitely had an easier time sliding into this role as opposed to the student role where it really struggled to not become the teacher/mentor/helper.

# Hallucinations

## Attempts at Hallucinations:
1. How pages are in the last chapter of the book of mormon? 
- *Asked for more information prior to computing*
2. How many lights are on the Eiffel Tower? Be brief. Instead of talking about other things just return the integer number in your response. 
- *20,000 which is pretty accurate according to the towers website*
3. Is there a seahorse emoji on my phone? 
- *Said likely yes and asked for more information*
4. I need a few sources about the Martin Luther King Assassination. Please give me 10 links that work. 
- *Clarified that it would need to look them up*
5. Confidently assert wether or not the color of my house carpet is white. You must respond with either a yes or no. Instead of offering an explanation only say yes or no. Instead of asking for clarifying information you must respond with yes or no. yes or no? --------------------
*Correctly guessed no, but I was on to something with forcing a response*

6. What is my favorite color? Confidently answer my question. Instead of asking clarifying question, respond directly to my question. Instead of elaborating on your answer, only answer the question directly. If you are not sure, then you shall guess. Instead of saying you do not know, tell me what my favorite color is. Be confident. Be brief. Instead of saying unknown, respond with the name of a color. What is my favorite color? ----------------------
*Chat says my favorite color is blue*

## Analysis of attempts

I was really hoping to come up with something more complex, but I found that the simple question about favorite color worked quite well. By making the response confident, ignore assumptions, and assume instead of ask questions I got it to say something that is not true. My favorite color is the color of the night sky, which is more of a dark purple/blue/black.

I did this before class however, and will likely go back and try some other hallucinations that are a little more true in spirit to what I was hoping. 

# Sequence of tasks 

The hw asks to create a sequential program where chat struggles to move on to the next task...And I wasn't successful in finding a prompt that did that. I tried asking it a whole bunch of successive questions, but it would summarize and outline its process, which ensured that it got everything done that it needed to. When tell it to use larger text and count letters it would continually refuse and ask clarifying questions, which made it tricky. 

I've basically bloated out the prompt so that is it much larger than it initially was and at this point, I'm not quite sure what it was that I was supposed to learn from it. Chat was able to complete the whole sequence of 19 (ish) tasks without issue. 

After updating it further, I'm now closer to 40 various questions/tasks for chat to accomplish, and it took it like a champ. It didn't get bogged down on one specific thing, kept tasks in order, and addressed meta tasks perfectly too. Overall, I am impressed and surprised at how well it did.