from dotenv import load_dotenv
load_dotenv() 
from flask import Flask, render_template, request , jsonify

from db_qq import get_gemini_response,read_sql_query,get_gemini_response_qa,prompt,input_prompt
from qaaa import  get_gemini_response_pa,input_prompt_pa,fetch_google_links
from resume import get_gemini_repsonse_resume,get_gemini_repsonse_role,cleanResume,input_prompt_resume,input_pdf_text,prompt_role
from decide_query import get_gemini_decision,decision_prompt
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#URL for response for previous year placement data
@app.route('/response_db',methods=['GET', 'POST'])
def response():
        global DATA
        question = request.args.get('msg')
        res_bot=get_gemini_response(question,prompt)
        print(res_bot)
        data=read_sql_query(res_bot)
        print(data)
        DATA = data
        answer=get_gemini_response_qa(question,input_prompt.format(data=DATA))
        print(answer)
        return answer




#URL for placement preparation
@app.route('/response_qa', methods=['GET', 'POST'])
def response_qa():
    input_msg = request.args.get('msg')
    response = get_gemini_response_pa(input_msg, input_prompt_pa)
    print(response)
    if "apologies" not in response.lower() and "sorry" not in response.lower() and "apologize" not in response.lower():

        # Call the fetch_google_links function
        links = fetch_google_links(input_msg)
        formatted_links = []
        for link in links:
            parsed_url = urlparse(link)
            domain = parsed_url.netloc.replace("www.", "")
            formatted_link = f"<a href='{link}'>{domain}</a>"
            formatted_links.append(formatted_link)
        # Add a line indicating the links are for reference in bold
        response_with_links = "<br><strong>Here are additional resources:</strong><br>"
        # Combine response and links
        response_with_links += "<br>".join(formatted_links)
        formatted_response = response + "<br>" + response_with_links  
        return formatted_response
    return response



#URL for resume parser
@app.route('/response_resume',methods=['GET','POST'])
def response_res():
    jd = request.form.get('msg')  # Add this line for debugging
    uploaded_file = request.files['file']     
    text = input_pdf_text(uploaded_file)
    cleaned_resume = cleanResume(text)
    response = get_gemini_repsonse_resume(cleaned_resume, input_prompt_resume.format(jd=jd)) # Add this line for debugging
    role=get_gemini_repsonse_role(cleaned_resume,prompt_role)
    return jsonify({'response': response, 'role': role})


@app.route('/decision_making',methods=['GET','POST'])
def make_decision():
    input=request.args.get('msg')
    res=get_gemini_decision(input,decision_prompt)
    print(res)
    return res

if __name__ == '__main__':
    app.run(debug=True)