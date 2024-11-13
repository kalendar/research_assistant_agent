import requests
from bs4 import BeautifulSoup
import time


# Run a local model so this is free!
# Replace with your endpoint
API_ENDPOINT = 'http://127.0.0.1:1234/v1/chat/completions'


# Read in arXiv URLs from urls.txt
with open("urls.txt", "r") as file:
    arxiv_urls = [line.strip() for line in file if line.strip()]


# Get articles from arXiv
def get_arxiv(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    # Get all <dt> and <dd> elements
    dt_elements = soup.find_all('dt')
    dd_elements = soup.find_all('dd')

    # Ensure they're paired correctly
    for dt, dd in zip(dt_elements, dd_elements):

        # Extract article URL from <dt>
        article_url = dt.find('a', title="Abstract")
        article_url = "https://arxiv.org" + article_url['href']

        # Extract other data from <dd>
        title = dd.find('div', class_='list-title mathjax').get_text(strip=True).replace('Title:', '').strip()
        abstract = dd.find('p', class_='mathjax').get_text(strip=True)

        # Append the data to the articles list
        articles.append({
            'title': title,
            'abstract': abstract,
            'article_url': article_url
        })

    return articles


# Check whether the articles are relevant or not
def check_relevance_with_llm(articles, processed_titles):

    headers = {
        "Content-Type": "application/json"
    }

    relevant_articles = []

    for article in articles:
        # Skip articles that have already been processed
        if article['title'] in processed_titles:
            continue

        # Read the prompt template from prompt.txt
        with open("prompt_template.txt", "r") as file:
            prompt_template = file.read()

        # Format the prompt with the article's title and abstract
        prompt = prompt_template.format(title=article['title'], abstract=article['abstract'])

        # Prepare request data for the API
        data = {
            # Replace with the name of the model you want to use
            "model": "xaskasdf/Llama-3.1-8b-instruct-gguf",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1,
            "temperature": 0
        }

        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        answer = response.json()["choices"][0]["message"]["content"].strip()

        if answer.lower() == "yes" or answer.lower() == "yes.":
            relevant_articles.append(article)

        # Mark this article as processed so we don't process it again
        processed_titles.add(article['title'])

        # Sleep a little between requests
        time.sleep(1)

    return relevant_articles


# Main function
def main():
    all_relevant_articles = []
    processed_titles = set()

    for url in arxiv_urls:
        print(f"Getting articles from {url}...")
        articles = get_arxiv(url)
        print(f"Found {len(articles)} articles. Checking their relevance...")

        relevant_articles = check_relevance_with_llm(articles, processed_titles)
        all_relevant_articles.extend(relevant_articles)
        print(f"Found {len(relevant_articles)} relevant articles in this category.\n")

    # Print the relevant articles
    if all_relevant_articles:
        print("Relevant Articles:")
        for article in all_relevant_articles:
            print(f"Title: {article['title']}")
            print(f"URL: {article['article_url']}")
            print(f"Abstract: {article['abstract']}\n{'-'*40}")
    else:
        print("No relevant articles found.")


if __name__ == "__main__":
    main()
