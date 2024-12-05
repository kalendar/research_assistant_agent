import requests
import ollama
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

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

# Check whether the articles are relevant or not using Ollama
def check_relevance_with_llm(articles, processed_titles):

    # List to store abstracts and their relevance answers for CSV
    csv_data = []

    for article in articles:
        # Skip articles that have already been processed
        if article['title'] in processed_titles:
            continue

        # Read the prompt template from prompt.txt
        with open("prompt_template.txt", "r") as file:
            prompt_template = file.read()

        # Format the prompt with the article's title and abstract
        prompt = prompt_template.format(title=article['title'], abstract=article['abstract'])

        # Use Ollama to get relevance
        response = ollama.generate(
            model="llama3.1:8b-instruct-q8_0",
            prompt=prompt
        )

        # Extract the response content
        answer = response['response'].strip().rstrip('.')

        # Save the abstract and answer to csv_data list
        csv_data.append({
            'title': article['title'],
            'article_url': article['article_url'],
            'abstract': article['abstract'],
            'answer': answer
        })

        # Mark this article as processed
        processed_titles.add(article['title'])

        # Sleep a little between requests
        time.sleep(1)

    return csv_data

# Main function
def main():
    processed_titles = set()
    csv_data = []

    for url in arxiv_urls:
        print(f"Getting articles from {url}...")
        articles = get_arxiv(url)
        print(f"Found {len(articles)} articles. Checking their relevance...")

        relevance_data = check_relevance_with_llm(articles, processed_titles)
        csv_data.extend(relevance_data)  # Add relevance data for CSV output
        print(f"Processed relevance check for {len(relevance_data)} articles in this category.\n")

    # Get current date and format it as "MM-DD-YYYY"
    current_date = datetime.now().strftime("%m_%d_%Y")
    filename = f"article_relevance_{current_date}.csv"

    # Write to CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ['answer', 'title', 'article_url', 'abstract']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

    print("CSV file written successfully.")

if __name__ == "__main__":
    main()
