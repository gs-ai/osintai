import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_and_search_keyword(start_url, keyword, max_depth=3):
    visited = set()  # Set to keep track of visited URLs
    to_visit = [(start_url, 0)]  # Queue of URLs to visit along with their depth
    found_keyword_urls = []  # List to store URLs where the keyword is found

    while to_visit:
        url, depth = to_visit.pop(0)  # Get the next URL and its depth

        if url not in visited and depth <= max_depth:
            try:
                response = requests.get(url)
                response.raise_for_status()
                visited.add(url)  # Mark this URL as visited

                # Parse the content with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Check if the keyword is in the page text
                if keyword.lower() in soup.get_text().lower():
                    found_keyword_urls.append(url)
                    print(f"Keyword found at: {url}")

                # Find all links and add them to the to_visit list
                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(url, link['href'])
                    if absolute_link not in visited:
                        to_visit.append((absolute_link, depth + 1))

            except requests.exceptions.RequestException as e:
                print(f"Error crawling {url}: {e}")

    # Write the results to a file
    filename = f"{keyword.replace(' ', '_')}_results.txt"
    with open(filename, 'w') as file:
        for url in found_keyword_urls:
            file.write(url + '\n')
    
    print(f"\nResults written to {filename}")
    return found_keyword_urls

# User input for the URL and keyword
user_input_url = input("Enter the URL to crawl: ")
user_input_keyword = input("Enter the keyword to search for: ")

# Example usage
found_urls = crawl_and_search_keyword(user_input_url, user_input_keyword, max_depth=3)
