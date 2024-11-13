# research_assistant_agent
This agent reads abstracts of preprints from arXiv.org and classifies them as relevant or irrelevant based on your criteria.

# Installation
To install the agent, you'll need:
* Python >= 3.12
* the libraries in the requirements.txt file
* an LLM running locally using a tool like LM Studio or ollama

# Configuration
To configure the agent, 
* Browse arXiv.org to find the categories you want to follow. Add the URL for the New page for each category you want to follow to the urls.txt file. (See example in the file.)
* Edit the prompt in the prompt_template.txt file so the agent knows what to look for when reading through abstracts.

# Using the Agent
* Run the agent from the command line with `python research_assistant_agent.py`. I recommend piping the output to a file, like `python research_assistant_agent.py > 11-12-2024..txt`. (You can schedule the script to run using cron or other scheduling software. If you know how to send email from a script, you can do that, too.)
* When the agent is done, browse through the text file to read the abstracts the agent classified as relevant. Then you can decide which full articles to read. 

