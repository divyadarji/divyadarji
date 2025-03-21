from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to scrape website content and links
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text content
        paragraphs = soup.find_all(["p", "h1", "h2", "h3"])
        content = "\n".join([p.get_text() for p in paragraphs])

        # Define social platforms
        social_platforms = ["linkedin", "twitter", "instagram", "github", "facebook", "youtube"]
        social_links = {}

        for a in soup.find_all('a', href=True):
            link_text = a.text.strip()
            link_url = a['href']

            # Match only social media links and avoid duplicates
            for platform in social_platforms:
                if platform in link_url.lower() or platform in link_text.lower():
                    social_links[platform] = f'<a href="{link_url}" target="_blank">{link_text or platform.capitalize()}</a>'

        return content[:3000], social_links  
    except Exception as e:
        print(f"Error scraping website: {e}")
        return "Could not retrieve website data.", {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"response": "No message provided"}), 400

        # Scrape website content and links
        website_url = "http://127.0.0.1:5500/aichatbot/portfolio2025/index.html"
        website_content, website_links = scrape_website(website_url)

        # Keep original prompt
        full_prompt = f'''assume that You are chatbot of website.
                        Use the following website information to answer the question in direct and short.
                        for example question is: hello then answer is I am xyz abc engineer what can i do for you :\n\n{website_content}\n\nUser: {user_message}'''

        response = model.generate_content(full_prompt)

        # Check if user asked for a specific social media link
        response_text = response.text
        requested_platform = None

        for platform in website_links.keys():
            if platform in user_message.lower():
                requested_platform = platform
                break

        if requested_platform:
            response_text = f"Here is my {requested_platform.capitalize()} link: {website_links[requested_platform]}"

        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"response": "Sorry, I'm having trouble processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
