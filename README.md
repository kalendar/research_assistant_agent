# research_assistant_agent
This agent reads abstracts of preprints from arXiv.org and classifies them as relevant or irrelevant based on your criteria.

# Setup
To get up and running you'll need:
* Python >= 3.11
* the libraries in the requirements.txt file
* an LLM running locally using a tool like [LM Studio](https://lmstudio.ai/) or [ollama](https://ollama.com)

# Configuration
To configure the agent, 
* Browse [arXiv.org](https://arxiv.org) to find the categories you want to follow. Add the URL for the New page for each category you want to follow to the urls.txt file. (See example in the file.)
* Edit the prompt in the prompt_template.txt file so the agent knows what to look for when reading through abstracts.

# Using the Agent
* Run the agent from the command line with `python research_assistant_agent.py`.
* Output is written to a date-named CSV file you can post-process however you like. The first column in the CSV includes a Yes or No, representing whether the reviewed article fit the review criteria outlined in the prompt_template.txt.
