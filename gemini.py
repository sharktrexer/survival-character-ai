import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

KEY = os.environ['API_KEY']

genai.configure(api_key=KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)