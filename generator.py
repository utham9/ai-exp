import google.generativeai as genai
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Function to fetch HTML content from a URL
def fetch_html(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        return response.text
    return None

# Function to extract button elements related to "Login"
def extract_login_button(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    buttons = soup.find_all(["button", "a"], string=lambda text: text and "login" in text.lower())
    
    if buttons:
        return str(buttons[0])  # Return first matched button
    return None

# Function to get response from Gemini Pro API
def get_gemini_response(prompt):
    if not API_KEY:
        raise ValueError("API Key not found. Please check your .env file.")
    
    # Configure API
    genai.configure(api_key=API_KEY)
    
    # Initialize Gemini Pro model
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    # Send the prompt and get the response
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    # Fetch HTML content from AngelOne
    url = "https://www.angelone.in/"
    html_content = fetch_html(url)
    
    if html_content:
        # Extract Login button HTML
        login_button_html = extract_login_button(html_content)
        
        if login_button_html:
            # Create a precise prompt
            prompt = f"Find the XPath for the following HTML element:\n{login_button_html}"
            
            # Get the response from Gemini Pro API
            xpath = get_gemini_response(prompt)
            
            # Print the extracted XPath
            print("XPath for 'Login' button:", xpath)
        else:
            print("Login button not found.")
    else:
        print("Failed to fetch HTML content from the URL.")
