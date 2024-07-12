# Q&A Chatbot

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urlsplit  
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response_pa(question,prompt):
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content([question,prompt])
    return res.text


def fetch_google_links(input):
    try:
        url = f"https://www.google.com/search?q={input}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        top_links = []
        domains = set()  # Keep track of unique domains
        for link in links:
            href = link.get("href")
            if href.startswith("/url?q="):
                full_url = href.split("/url?q=")[1].split("&sa=")[0]
                # Exclude map links, YouTube videos, and other undesired links
                if full_url.startswith("https://") and not full_url.startswith("https://www.google.com/maps") and not full_url.startswith("https://maps.google.com/maps") and "youtube.com/watch" not in full_url and "google.com/search" not in full_url:
                    domain = urlparse(full_url).netloc
                    if domain not in domains:  # Check if domain is already fetched
                        top_links.append(full_url)  # Append only the full URL
                        domains.add(domain)
            if len(top_links) == 5:  # Stop when you have the top 5 links
                break
        return top_links
    except Exception as e:
        print("An error occurred:", e)
        return []



def encode_domain_with_path(url):
    # Extract domain name and path from the URL
    parsed_url = urlparse(url)
    domain_with_path = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return domain_with_path


input_prompt_pa= """

Your task is to serve as a placement bot, providing concise and valuable assistance to students in preparing for placements and navigating the job search process effectively. 
You should offer guidance on various placement-related topics such as the placement process, job search strategies, resume building, interview preparation, company-specific interview tips and questions, 
recruitment processes, number of interview rounds in companies, how to get placed in specific companies, how to get a job in those companies. Additionally, provide previous year question papers, previous year hiring processes, 
and previous year interview questions tailored to assist students in their preparation for placements. If a student asks about how to prepare for a specific company like BetSol or how to get a job there,
provide brief and helpful advice and tips. However, if the question is not directly related to recruitment, placements, or education, respond with "Apologies" or "Sorry" only and provide a reason for not answering the question. 
Remember to prioritize placement-related, company-related, and job-related inquiries, and respond promptly with concise, accurate, and informative answers, not exceeding 5 lines, to support students effectively in their placement preparation journey.
"""

























































































































































