# GUI for LLM interactions

I have a default react + vite typescript boilerplate app that I am running locally using the default settings. I want you to write a simple GUI for interacting with any LLM in typescript. Please only include necessary output for the app.tsx file your response. 

GUI should have five parts:
-------------------
1. one intuitive part where I can just write a question or thought to the LLM. I need the common functionality where I am able to type multiline text, and submit it to an LLM of my choice. The default option should be a preconfigured OpenAI API.


*The next three sections (2-4) are very similar and deals with md files that will be put together to make a more algorithmic prompt in the last section.*

2. Section where I can compose prompts and save them locally. The app.tsx is in a folder called GUI/src and should save prompts under GUI/prompts. 

3. Section to save inputs for prompts of both text, and md. This section will be saved locally under GUI/inputs.

4. Section for saving specified structure files, which could include a description of json file format or html along with sufficient instruction to ensure that output is structured correctly.

5. The last section has an interface where I can pick a prompt from the files locally, input text, and specified structure to make my own complete prompt to an LLM using the same api information that I would in the first part. This part of the GUI lets me pick and chose each of the the options I want for the prompt, with the input text and structure being optional. It will then make the query for me and display the output on the screen like the first part does.