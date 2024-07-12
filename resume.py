import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse_resume(text,input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([text,input])
    return response.text

def get_gemini_repsonse_role(cleaned_resume,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([cleaned_resume,prompt])
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

def cleanResume(txt):
    cleanTxt = re.sub('http\S+\s', ' ' ,txt)
    cleanTxt = re.sub('RT|cc',' ',cleanTxt)
    cleanTxt = re.sub('@\S+',' ',cleanTxt)
    cleanTxt = re.sub('#\S+\s',' ',cleanTxt)
    cleanTxt = re.sub('[%s]' % re.escape("""["#$%&*'()+,-./;:<=>?@[\]^_`{|}~"""),' ',cleanTxt)
    cleanTxt = re.sub(r'[^\x00-\x7F]',' ',cleanTxt)
    cleanTxt = re.sub('\s+',' ',cleanTxt)
    return cleanTxt




prompt_role=""" Predict the 3 job roles that candidate can look for based on the given resume and highlight the most suitable role
         
            """



input_prompt_resume='''Hey act like a skilled or very experienced ATS(Application Tracking System)
    with a deep understanding of tech field, software engineering, data science, data analyst, and big data engineer.
    Your task is to evaluate the resume based on the given job description .
    You must consider the job market is very competitive and you should provide best assistance for improving
    the resume in brief 2 lines maximum. Provide matching percentage based on jd ,Missing keywords with highest accuracy,Profile summary,Best assistance for chances of success,. 
    
    description:{jd}
    
    '''


















































































































































































