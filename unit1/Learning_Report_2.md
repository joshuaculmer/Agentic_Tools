# Improving from previous programs

## Structured Output
Structuring the output was pretty easy, I wrote a prompt that specified that all output was to be formatted in Json and gave it several generic examples. I wrote the Json Structure prompt for general use in various problems and included a line at the end that specified a master example that should be followed most closely. These master examples are specific examples tailored depending on usecase.

Using this combination of a generic structure prompt with a specific example, Chat was able to consistently provide output that matched my expectations. 

I added these two new parameters to my response.py file.

## Successful Diciphering of my text
I also returned to the problem that I worked on last time of getting chat to decipher a jumbled string of letters.

I refined the prompt to include a division of the words that it deciphered to ensure that there was more thorough reasoning for each word and that each letter was accounted for. This word division greatly improved the likelyhood that it would be able to find any words at all, but it was still not 100% accurate.


The new prompt also asked for a complete letter count of both the diciphered message and the initial encoded message, but that didn't make much of a difference. It didn't seem to use it in its logic/reasoning at all and would jsut hallucinate that it had the proper number of letters when enumerating them. This hallucinated value would be close to how many letters were either the encoded or decoded message, but not exactly.

I also included a reasoning protion where chat had to explain its reasoning for coming up with the diciphered text. This reasoning was listed in various locations in the json example, which may have an effect on the output but due to the high failure rate of the prompt I was not able to see a clear correlation.

Although not perfect, it was much closer to the original deciphered text than previous attempts.

{
  "initial encoded message": "wahtfiiximdelalhetteltresrodrepu",
  "deciphered message": "what if i mix all the letters reorder up",
  "divided words in deciphered message": ["what", "if", "i", "mix", "all", "the", "letters", "reorder", "up"],
  "Reasoning": "The string can be partitioned into word boundaries such that each segment is an anagram of a common English word. The first four letters "waht" can be rearranged to "what". The last two letters "pu" can be rearranged to "up". The remaining middle segment can be segmented into valid words in order: what | if | i | mix | all | the | letters | reorder | up. Each segment is a permutation of its corresponding target word, consistent with the constraint that letters do not cross word boundaries.",
  "initial letter count": {
    "a": 2,
    "d": 2,
    "e": 5,
    "f": 1,
    "h": 2,
    "i": 3,
    "l": 3,
    "m": 1,
    "o": 1,
    "p": 1,
    "r": 3,
    "s": 1,
    "t": 4,
    "u": 1,
    "w": 1,
    "x": 1
  },
  "deciphered letter count": {
    "a": 2,
    "d": 2,
    "e": 5,
    "f": 1,
    "h": 2,
    "i": 3,
    "l": 3,
    "m": 1,
    "o": 1,
    "p": 1,
    "r": 4,
    "s": 1,
    "t": 4,
    "u": 1,
    "w": 1,
    "x": 1
  }
}
48.56 seconds elapsed
----------- Usage ------------
Model: gpt-5-nano
Input (tokens): 1122
Cached (tokens): 0
Output (tokens): 4604
Reasoning (tokens): 4160
Total cost (USD): $0.001898


Another simlilarly close output:
--------------------------------
{
  "initial encoded message": "wahtfiiximdelalhetteltresrodrepu",
  "initial letter count": {
    "a": 6,
    "b": 0,
    "d": 3,
    "e": 6,
    "f": 2,
    "h": 3,
    "i": 5,
    "l": 5,
    "m": 2,
    "o": 1,
    "p": 1,
    "r": 4,
    "s": 1,
    "t": 6,
    "u": 1,
    "w": 1,
    "x": 2
  },
  "divided words in deciphered message": ["what", "if", "i", "fix", "all", "the", "letters", "ordered", "up"],
  "deciphered message": "what if i fix all the letters ordered up",
  "deciphered letter count": {
    "a": 6,
    "b": 0,
    "d": 3,
    "e": 6,
    "f": 2,
    "h": 3,
    "i": 5,
    "l": 5,
    "m": 2,
    "o": 1,
    "p": 1,
    "r": 4,
    "s": 1,
    "t": 6,
    "u": 1,
    "w": 1,
    "x": 2
  },
  "Reasoning": "The string can be partitioned into words such that each segment is an anagram of a common English word. The first four letters 'waht' rearrange to 'what', the next four can rearrange to form 'if' + 'i' or 'fi'/'ix' depending on boundary; continuing in this manner, the entire string can be split into: what | if | i | fix | all | the | letters | ordered | up. This respects the constraint that letters do not move beyond the initial word boundary and yields a coherent English sentence beginning with 'what' and ending with 'up'."
}
14.34 seconds elapsed
----------- Usage ------------
Model: gpt-5-nano
Input (tokens): 1122
Cached (tokens): 0
Output (tokens): 1946
Reasoning (tokens): 1472
Total cost (USD): $0.000835

Both of these responses incorrectly match the initial letter count and the diciphered letter count, and are off by a few letters. 

However, these two prompts were the only ones that were actually able to do any sort of diciphering. After testing it several more times I was unable to get it to produce consistent results, despite using the same prompts, structure, and examples as input.

There were a few others that at least gave an attempt, sometimes order would become together or _______ but most of its responses asked for additional clarification or additional parameters before it would be able to continue deciphering. 

All of these prompts were run on gpt-5-nano with low effort, which represents a major improvement in the prompts efficiency, since low effort was unable to yield any results with my old prompts that I submitted in the previous assignment. 

## Initial GUI

I also started setting up my own simple GUI to be able to interact with Chat using my program. I wrote two prompts to get started and will continue to work on this in my own time. 

### TypeScript Boiler Plate
The first prompt was to write a bash script that makes a new directory for the GUI, initializes a default react + vite typescript project, and starts the webpage via npm run dev. It did a decent job, but had a couple of issues when I tried to run it. This issue of response code not running upon generation leads me to wonder if I can automate an error checker, a second prompt that takes the first prompt's response as input and just validates its work based on my needs. I look forward to improving my knowledge of LLM workflows and think this would be a really cool thing to work on in the future.

### 5 Part GUI in app.tsx
The second prompt for my GUI was a one shot request to make a GUI with sections for basic prompts, storing prompts, storing structure prompts, storing examples, and advanced prompts where a prompt, structure, and example could be compiled into a single prompt. 

The app made several assumptions about design (it looked lousy) and did not integrate directly with my other program that I had written. I need to go back and continue to improve on this prompt by specifying the preexisting files that I have, interface design, and where the program will access my api key for it to work as intended.