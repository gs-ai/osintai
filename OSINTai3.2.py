import os
import random
import time
import subprocess
import re
from bs4 import BeautifulSoup
import requests

class WebCrawler:
    def __init__(self, seed_url, max_depth, max_urls, user_agents_file, search_terms=None):
        self.seed_url = seed_url
        self.max_depth = max_depth
        self.max_urls = max_urls
        self.user_agents = self.load_user_agents(user_agents_file)
        self.visited_urls = set()
        self.search_terms = search_terms

    def load_user_agents(self, user_agents_file):
        with open(user_agents_file, 'r') as file:
            user_agents = [line.strip() for line in file]
        return user_agents

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def fetch_url(self, url):
        headers = {'User-Agent': self.get_random_user_agent()}
        response = requests.get(url, headers=headers)
        return response

    def parse_links(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def search_in_content(self, html_content):
        if self.search_terms:
            return any(term.lower() in html_content.lower() for term in self.search_terms)
        return False

    def sanitize_filename(self, url):
        return re.sub(r'[^A-Za-z0-9]+', '_', url)

    def crawl(self):
        from typing import Any, Literal
        
        urls_to_visit: list[tuple[Any, int]] = [(self.seed_url, 0)]
        crawled_urls = []

        while urls_to_visit and len(self.visited_urls) < self.max_urls:
            current_url, depth = urls_to_visit.pop(0)
            if current_url in self.visited_urls or depth > self.max_depth:
                continue

            try:
                response = self.fetch_url(current_url)
                if response.status_code == 200:
                    html_content = response.text
                    links = self.parse_links(html_content)
                    for link in links:
                        if link not in self.visited_urls:
                            urls_to_visit.append((link, depth + 1))

                    self.visited_urls.add(current_url)
                    crawled_urls.append(current_url)
                    print(f"Crawled: {current_url}")

                    if self.search_in_content(html_content):
                        print(f"Search term found in: {current_url}")

                    # Interact with Ollama Gemma locally
                    self.analyze_with_gemma(current_url, html_content)

            except Exception as e:
                print(f"Failed to fetch {current_url}: {e}")

            time.sleep(random.randint(1, 3))

        return crawled_urls

    def analyze_with_gemma(self, url, html_content):
        filename = self.sanitize_filename(url) + ".txt"

        # Run the Gemma model on the content
        try:
            result = subprocess.run(
                ["ollama", "run", "gemma:7b"],
                input=html_content,
                text=True,
                capture_output=True
            )

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"URL: {url}\n\n")
                if result.returncode == 0:
                    analyzed_content = result.stdout
                    file.write("Analyzed with Gemma:\n")
                    file.write(analyzed_content)
                    file.write("\n\n")

                    # Compare the original HTML content with the analyzed content
                    variations = self.compare_content(html_content, analyzed_content)
                    file.write("Variations found:\n")
                    file.write(variations)
                else:
                    print(f"Failed to analyze with Gemma: {result.stderr}")
                    file.write(f"Failed to analyze with Gemma: {result.stderr}")

        except Exception as e:
            print(f"Error analyzing {url} with Gemma: {e}")

    def compare_content(self, original_content, analyzed_content):
        original_text = self.extract_text_from_html(original_content)
        variations = []
        analyzed_lines = analyzed_content.splitlines()

        for line in analyzed_lines:
            if line.strip() and line not in original_text:
                variations.append(line)

        return "\n".join(variations)

    def extract_text_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return lines

if __name__ == "__main__":
    seed_url = input("Enter the seed URL to start crawling: ")
    max_depth = int(input("Enter the maximum depth for crawling: "))
    max_urls = int(input("Enter the maximum number of URLs to crawl: "))
    user_agents_file = "user_agents.txt"
    search_terms = input("Enter search terms (comma-separated) or press enter to skip: ").split(',')

    search_terms = [term.strip() for term in search_terms if term.strip()]

    crawler = WebCrawler(seed_url, max_depth, max_urls, user_agents_file, search_terms)
    crawled_urls = crawler.crawl()
    print(f"Crawled URLs: {crawled_urls}")
