import os
import random
import time
import subprocess
from bs4 import BeautifulSoup
import requests

class WebCrawler:
    def __init__(self, seed_url, max_depth, max_urls, user_agents_file):
        self.seed_url = seed_url
        self.max_depth = max_depth
        self.max_urls = max_urls
        self.user_agents = self.load_user_agents(user_agents_file)
        self.visited_urls = set()

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

    def crawl(self):
        urls_to_visit = [(self.seed_url, 0)]
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

                    # Interact with Ollama Gemma locally
                    self.analyze_with_gemma(current_url, html_content)

            except Exception as e:
                print(f"Failed to fetch {current_url}: {e}")

            time.sleep(random.randint(1, 3))

        return crawled_urls

    def analyze_with_gemma(self, url, html_content):
        # Save the HTML content to a temporary file
        temp_html_file = "temp_content.html"
        with open(temp_html_file, 'w', encoding='utf-8') as file:
            file.write(html_content)

        # Run the Gemma model on the content
        try:
            result = subprocess.run(
                ["ollama", "run", "gemma:7b", "--input", temp_html_file],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"Analyzed with Gemma: {url}")
                print(result.stdout)
            else:
                print(f"Failed to analyze with Gemma: {result.stderr}")

        finally:
            # Clean up the temporary file
            os.remove(temp_html_file)

if __name__ == "__main__":
    seed_url = "https://example.com"
    max_depth = 2
    max_urls = 10
    user_agents_file = "user_agents.txt"

    crawler = WebCrawler(seed_url, max_depth, max_urls, user_agents_file)
    crawled_urls = crawler.crawl()
    print(f"Crawled URLs: {crawled_urls}")
