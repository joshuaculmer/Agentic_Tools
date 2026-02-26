# Getting setup

It took me a minute to configure the Chatbot with weather app to work as intended. In the ChatAgent, its check_for_tool_call() continue part of the loop wasn't working as I thought it would, so I had to adjust it some to get it working out of the box.

# Statsbot

So the stats bot that I made was not an improvement over the base model, it likely has some sort of automatic tool calling that it is using. It was able to provide detailed and accurate statistical information about a sequence of numbers.

# WebChatbot or ISS bot

Next thing chatbot that I built was a bot that could get ISS coordinates via API request. This worked pretty well, it was able to convert the coordinates to geospatial locations and use the url to get up to date information.

I spent a fair amount of time here looking into various free and public api's that I could find, this was one of the cooler ones.

# Scripture bot

Took me a little bit of time to interface with https://scriptures.byu.edu because I wanted to be able to query both scripture and conference talks. I had to structure the requests and parse its responses. The AI was able to adequately query scriptures.byu.edu and it worked great.
