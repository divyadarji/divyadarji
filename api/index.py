# api/index.py
from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all text from <p> and <h> tags
        paragraphs = soup.find_all(["p", "h1", "h2", "h3"])
        content = "\n".join([p.get_text() for p in paragraphs])

        return content[:3000]  # Limit to first 3000 characters (Gemini's context limit)
    except Exception as e:
        print(f"Error scraping website: {e}")
        return "Could not retrieve website data."

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
        
        # Scrape your portfolio website
        website_url = "http://127.0.0.1:5500/aichatbot/portfolio2025/index.html"  # Change this to your real website URL
        website_content = scrape_website(website_url)

        # Generate response using Gemini with website context
        full_prompt =f'''assume that You are chatbot of website.
                        Use the following website information to answer the question in direct and short.
                       for example question is: hello then answer is I am xyz abc engineer what can i do for you :\n\n{website_content}\n\nUser: {user_message}'''
        response = model.generate_content(full_prompt)
        
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"response": "Sorry, I'm having trouble processing your request."}), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True)
