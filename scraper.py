import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content
        text_content = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])

        # Define social media platforms to filter
        social_platforms = ["linkedin", "twitter", "instagram", "github", "facebook", "youtube"]
        social_links = {}

        for a in soup.find_all('a', href=True):
            link_text = a.text.strip()
            link_url = a['href']

            # Match only social media links
            for platform in social_platforms:
                if platform in link_url.lower() or platform in link_text.lower():
                    social_links[platform] = f'<a href="{link_url}" target="_blank">{link_text or platform.capitalize()}</a>'

        return text_content, social_links

    return "Failed to fetch content", {}

# Example: Scrape your portfolio website
portfolio_url = "http://127.0.0.1:5500/aichatbot/portfolio2025/index.html"
website_text, website_links = scrape_website(portfolio_url)

# Save scraped content
with open("website_content.txt", "w", encoding="utf-8") as file:
    file.write(website_text + "\n\nLinks:\n" + "\n".join(website_links.values()))

print("Website content and social media links scraped successfully!")
