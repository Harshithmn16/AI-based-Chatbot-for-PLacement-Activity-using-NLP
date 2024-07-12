from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import os
import sqlite3


import google.generativeai as genai
## Configure Genai Key



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))        
    
prompt=[
    """
     You are an expert in converting English questions to SQL query!
        The SQL database has the name BE_2022,BE_2023,Internship_2022,Internship_2023,MBA_2022,MBA_2023 and has the following columns - "S.No." INTEGER,
    "Date Of Drive",Drive,Type ,"Company Name",CSE ,ISE ,ECE ,"E&I" ,ME,IEM ,CVL ,PG ,SINGLE ,MULTIPLE ,TOTAL,
    "CTC OFFERED (in Lakhs)","Branches","Eligible Criteria",

    \n  Example 1 - How many entries of records are present?, 
        the SQL command will be something like this SELECT COUNT(*) FROM BE_2023 ; 
    
    \n  Example 2 - What is the highest ctc?, 
        the SQL command will be something like this SELECT MAX(CAST(REPLACE("CTC OFFERED (in Lakhs)", ',', '') AS DECIMAL(10,2))) AS Highest_CTC FROM BE_2023;

    \n  Example 3 -
        How many students have been placed in betsol from cse ? the SQL command will be something like this SELECT SUM(CSE) AS Students_Placed
        FROM BE_2023
        WHERE "Company Name" = 'Betsol';

    \n  Example 4-
        list 5  companies offered highest ctc or package ? the SQL command will be something like this 
        SELECT "Company Name" FROM BE_2023 ORDER BY CAST(REPLACE("CTC OFFERED (in Lakhs)", ',', '') AS DECIMAL(10,2)) DESC LIMIT 5;
        
    \n Example 5 which company hired the most CSE students ? the SQL command will be something like this SELECT "Company Name" 
       FROM BE_2023
       WHERE "Company Name" IS NOT NULL
       GROUP BY "Company Name"
       ORDER BY  SUM(CSE) DESC
       LIMIT 1;

    \n Example 6 how many CSE students were placed and which company hired the most CSE students ? the SQL command will be something like this SELECT Company_Name, SUM(CSE) AS Total_CSE_Placements
       FROM BE_2023
       WHERE "Company Name" IS NOT NULL
       GROUP BY "Company Name"
       ORDER BY Total_CSE_Placements DESC
       LIMIT 1;

    \n Example 7 what is the eligible crieteria was betsol ? the sql command will be like SELECT "Eligible Criteria"
       FROM BE_2023
       WHERE "Company Name" = 'Betsol';

    \n Example 8 From which branches did betsol hired ? the sql command be like SELECT DISTINCT Branches AS Branch
       FROM BE_2023
       WHERE "Company name" = 'Betsol';

    \n Example 9 How many students are placed in kickdrum ? the sql command will be 
       SELECT SUM(CSE + ISE + ECE + "E&I" + ME + IEM + CVL + PG) AS Students_Placed
       FROM BE_2023
       WHERE "Company Name" = 'Kickdrum';
 
    \n Example 10 which companies visited campus in 2023? the sql command be like SELECT DISTINCT "Company Name"
        FROM BE_2023
        UNION
        SELECT DISTINCT "Company Name"
        FROM Internship_2023 UNION SELECT DISTINCT "Company Name" FROM MBA_2023 WHERE Drive='On Campus'; 

    \n Example 11 which year did most of cse studnets placed? the sql command be like SELECT Year, SUM(CSE) AS Total_CSE_Placements
        FROM (
            SELECT 2022 AS Year, CSE FROM BE_2022
            UNION ALL
            SELECT 2023 AS Year, CSE FROM BE_2023
        ) AS CombinedData
        GROUP BY Year
        ORDER BY Total_CSE_Placements DESC
        LIMIT 1;

    \n Example 12 Which companies visited in both 2022 and 2023  the sql command be like SELECT "Company Name"
        FROM BE_2022
        WHERE "Company Name" IN (SELECT "Company Name" FROM BE_2023)
        ORDER BY RANDOM(); 

    \n Example 13 which  companies offered internship and job offer ? the sql command be like SELECT "Company Name"
        FROM BE_2023
        INTERSECT
        SELECT "Company Name"
        FROM Internship_2023;

    \n Example 14 which company offered highest stipend ? the sql command be like SELECT MAX(CAST(REPLACE("Stipend (Per Month)", ',', '') AS DECIMAL(10,2))) AS Highest_Stipend FROM Internship_2023;
       LIMIT 1;

    \n Example 15 how many months of internship does kickdrum provide ? the sql command be like SELECT "Duration"
       FROM Internship_2023
       WHERE "Company Name" = 'Kickdrum';

    \n Example 16 in which year most of ece students got placed and in which company ? the sql command be like SELECT Year, "Company Name", SUM(ECE) AS Total_ECE_Placements
        FROM (
            SELECT 2022 AS Year, "Company Name", ECE FROM BE_2022
            UNION ALL
            SELECT 2023 AS Year, "Company Name", ECE FROM BE_2023
        ) AS CombinedData
        GROUP BY Year, "Company Name"
        ORDER BY Total_ECE_Placements DESC
        LIMIT 1;
    
    \n Example 17 which year has most companies visit ? the sql command be like SELECT
        Year,COUNT(DISTINCT "Company Name") AS Total_Companies FROM (
        SELECT 2022 AS Year,"Company Name" FROM BE_2022 WHERE  Drive = 'on campus'
        UNION ALL SELECT 2023 AS Year,"Company Name" FROM BE_2023 WHERE Drive = 'on campus'
        ) AS CombinedData GROUP BY Year ORDER BY Total_Companies DESC
        LIMIT 1;

    \n Example 18 Which all companies hired for internship on campus in 2023? the sql command be like SELECT DISTINCT "Company Name"
       FROM Internship_2023
       WHERE "Drive" = 'On Campus';

    \n Example 19 Which comapnies visited in April 2022 ? the sql command be like SELECT DISTINCT "Company Name"
       FROM BE_2022
       WHERE "Date Of Drive" LIKE '%04/2022%'
       AND Drive = 'On Campus';

    \n Example 20 How many students placed in 2023 ? the sql command be like SELECT SUM(total) AS total_students_placed
       FROM BE_2023;





   also SQL query should not have " ``` "in beginning or end and sql word in output

    """ 
]




## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql):
    conn=sqlite3.connect("Placement_training.db")
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    # for row in rows:
    #     print(row)
    return rows

def get_gemini_response_qa(question,input_prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([question,input_prompt])
    return response.text


input_prompt = """Given a question and its corresponding answer(s) {data}, generate a response that incorporate {data} as the answer(s) to a question in a coherent sentence.
For example 1, if the question is: "Which fruits are red?" and {data} = ["Apple", "Cherry"], the response should be: "The fruits that are red are 
1 Apple 
2 Cherry."
For example 2, if asked to provide 5 companies that hired the most number of ECE students and {data} = [('Cognizant',), ('LTI  Level 0',), ('DXCorr',), ('Continental (Core)',), ('Vitesco Technologies (Core)',)], the response should list the top 5 companies as follows:
1. Cognizant
2. LTI  Level 0
3. DXCorr
4. Continental (Core)
5. Vitesco Technologies (Core)
Adapt this prompt to handle various types of answers for the question asked , including cases where the answer may be a single item or a list of items, and produce appropriate responses.
"""













































































































