
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import os
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import requests

#Create a .env file in your workspace and get your Google API Key passed in to the file
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_decision(question,prompt):
   model = genai.GenerativeModel('gemini-pro')
   res = model.generate_content([question,prompt])
   return res.text



decision_prompt="""You role is to decide the given question should be sent to which function. There are 2 functions available:

1. "response_db": This function handles user queries related to previous placements of the college. Examples of such queries include:
   - "How many students were placed in Kickdrum?"
   - "What is the highest package offered?"
   - "List the companies which hired most of the CSE students."

2. "response_qa": This function handles general placement-related queries. Examples include:
   - "How to prepare for placements?"
   - "How to improve my resume?
   - "how to get placed in kickdrum?
   - previous year interview questions of zscaler ?
   - "which topics to focus on to clear the onlines assessment of particular company"

Please respond with whether the user input should be passed to the which function "response_db" function or the "response_qa" function, based on the context of the question.
give response only function in lower case.
"""









