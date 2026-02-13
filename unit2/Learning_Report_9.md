# Setup

I ended up having to run a little bit more code than anticipated to get everything set up. And understand how fire works, ie. taking input parameters, took a fair bit too. But after that, it was pretty easy to get ChromaDB working and downloadgctalks to perform as intended.

```
pip install fire
```

I also ended up debugging a little bit with the file path in python that was struggling, but it ended up working just fine outside of VScode's terminal.

# Chat Bot

I ingested the past years worth of conference talks via the script that was given from the lecture downloads. I wrote a prompt for the conference chatbot, didn't spend much time on it, but it sufficed. Then wrote a function single_query() that could take a system prompt, RAG information, query, model, effort, and potentially complete history. 

It worked great! I was able to ask about why faith was important and what President Nelson's most recent address was. It did a good job at both of them.