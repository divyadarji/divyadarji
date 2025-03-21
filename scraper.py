import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = ' '.join([p.text for p in soup.find_all('p')])  # Extracting paragraphs
        return text_content
    return "Failed to fetch content"

# Example: Scrape your portfolio website
portfolio_url = "http://127.0.0.1:5500/aichatbot/portfolio2025/index.html"  # Change this if needed
website_text = scrape_website(portfolio_url)

# Save scraped content to a file
with open("website_content.txt", "w", encoding="utf-8") as file:
    file.write(website_text)

print("Website content scraped and saved!")
