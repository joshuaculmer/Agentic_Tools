# The Setup

I started off with the boilerplate that was gone over in class and created the first three functions in basic_embedding.py, which were embed(), compare_embeddings_plot(), and search_phrases().

I then wrote two prompts, one to add additional feature, and another to flesh out my embeddings capability and make converting raw text files into embeddings, then storing the embeddings for future use. It worked alright, I used claude to iron out some of the kinks, which is the current state of basic_embedding.py

# What I did with the Embedding tools

I went to [gutenberg.org](https://gutenberg.org/cache/epub/1184/pg1184.txt) and yoinked their whole text for The Count of Monte Cristo. Its the unabridged version and is a great read. I used this to test that the embeddings program worked as intended. There was an issue with creating too many embeddings at once, due to OpenAI's max input token limitations. This lead to an additional edit where I batch requested 100 embeddings at a time, which had no issue.

I then queried the embeddings. My first query was suggested by Claude in the code that it gave me, so I asked "What happened to Edmond Dantes". Initially I wasn't super impressed by the responses, but then I remembered what the responses actually mean. Its not asking a bot to answer the question, its querying the book for sections that are closely aligned with the meaning of the question. Viewed in that light, it did pretty good.

Next I quiered "poison", which lead to pretty expected results. I then asked for "divine justice" and it did fantastic. There were several sections that embodied moments in the book where divine justice was dealt but not explicitly mentioned.

# Chunking

Reading through the results from the queries, I felt like the chunks worked well for this book, even though there were times where it felt like it didn't work because of the buffer. The size of 1000 characters worked well. I also included an option to adapt this size, but in the future I would like to work with other chunking algorithms that can account for syntatic differences, like verses of scripture, or complete paragraphs, instead of a block of text of a given length.
