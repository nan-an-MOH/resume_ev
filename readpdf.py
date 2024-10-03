from PyPDF2 import PdfReader
from os import listdir
from os.path import join, isfile
from openai import OpenAI
import os
from chatgpt import *
from fuzzy import *
import pandas as pd

OPENAI_API_KEY = "-"
os.environ["OPENAI_API_KEY"] = "-"

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo-0125"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

resume_dir = "resume_confidencial"

def extract_text(pdf_reader):
    """
    extract the pdf text 
    """

    full_text = ""

    # Iterate through each page
    for page_num, page in enumerate(pdf_reader.pages, start=1):
        # Extract text from the page
        text = page.extract_text()

        page_text = f"\nPage {page_num}\n{text}"

        # Concatenate the extracted text with the full text
        full_text += page_text

    if not check_malicious(full_text):
        raise Exception('Malicious text detected')

    query = f""" The text below contains cover letter, resume, and transcripts of a candidate.

        Article:
        \"\"\"
        {text}
        \"\"\"

        The page number is mentioned at the beginning of each page
        Can you store the starting page numbers of cover letter, resume and transcripts respectively in a comma-separated list of numbers.
        Please do not add any other text in the response generated.

        """

    response = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': 'Give information based on the resume and transcripts text'},
            {'role': 'user', 'content': query},
        ],
        model=GPT_MODEL,
        temperature=0
    )

    response_text = response.choices[0].message.content

    start_pages = list(map(int, response_text.split(',')))

    resume_start = start_pages[1]
    transcripts_start = start_pages[2]

    resume_text = ""

    # Iterate through each page again and extract the resume text
    for page_num, page in enumerate(pdf_reader.pages, start=1):
        if resume_start <= page_num < transcripts_start:
            resume_text += page.extract_text()

    transcripts_text = ""

    for page_num, page in enumerate(pdf_reader.pages, start=1):
        if page_num >= transcripts_start:
            transcripts_text += page.extract_text()


    return [full_text, resume_text, transcripts_text]

def readback():
    '''
    returns the list of names and pdf content of all resumes
    '''
    resumes = [[f[:-11], extract_text(PdfReader(join(resume_dir, f)))] 
           for f in listdir("resume_confidencial") if isfile(join(resume_dir, f))]
    return resumes

# for debugging
if __name__ == "__main__":
    cvs = readback()
    output = pd.DataFrame(columns=['workexp', 'transcript', 'skill_r1', 'skill_r2', 'skill_r3', 'extrum'])
    for cv in cvs:
        row = []
        row.append(ask_resume(cv[1][1]))
        row.append(ask_transcript(cv[1][2]))
        row.append(evaluate(skills_ds_p1, cv[1][0]))
        row.append(evaluate(skills_ds_p2, cv[1][0]))
        row.append(evaluate(skills_ds_p3, cv[1][0]))
        row.append(evaluate(extracurricular, cv[1][0]))
        output.loc[cv[0]] = row
    print(output)