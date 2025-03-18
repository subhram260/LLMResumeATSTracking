from dotenv import load_dotenv

load_dotenv()
import subprocess
from pdf2docx import Converter
import streamlit as st
import os
from PIL import Image
import io
import pdf2image
import base64
import fitz

import google.generativeai as genai


# Everything is accessible via the st.secrets dict:
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the PDF file
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        # Initialize a list to hold the text of each page
        text_parts = []

        # Iterate over the pages of the PDF to extract the text
        for page in document:
            text_parts.append(page.get_text())

        # Concatenate the list into a single string with a space in between each part
        pdf_text_content = " ".join(text_parts)
        return pdf_text_content
    else:
        raise FileNotFoundError("No file uploaded")


def generate_pdf(latex_code, output_pdf="output.pdf"):
    with open("temp.tex", "w") as f:
        f.write(latex_code)

    # try:
        subprocess.run(["pdflatex", "temp.tex"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "temp.pdf" if os.path.exists("temp.pdf") else None
    # except Exception as e:
    #     return None

def generate_word(latex_code, output_docx="output.docx"):
    with open("temp.tex", "w") as f:
        f.write(latex_code)

    # try:
        subprocess.run(["pandoc", "temp.tex", "-o", output_docx], check=True)
        return output_docx if os.path.exists(output_docx) else None
    # except Exception as e:
    #     return None

## Streamlit App

st.set_page_config(page_title="Resume Expert")

st.title("Smart ATS")
st.text("Improve Your Resume ATS")
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("What are the Keywords That are Missing")

submit4 = st.button("Percentage match")

submit5 = st.button("Skill Alignment Table Generator")

submit6 = st.button("LatexResume Generator")


input_promp = st.text_input("Queries: Feel Free to Ask here")

submit = st.button("Answer My Query")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an Technical Human Resource Manager with expertise in data science, 
your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. 
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
 assess the compatibility of the resume with the role. Give me what are the keywords that are missing
 Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development.
"""
input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt5 ="""
Evaluate the alignment of technical skills and experience with the provided job description in a tabular format. 
Use the following structure:  
Technical Skills Comparison Create a table with the following columns:  
Required Skill: List the skills required as per the job description.  
Candidate's Skills/Resume: Indicate if the skill exists in the resume. 
Provide supporting context if available.  
Match: Use ✅ for full match, ⚠ for partial match, and ❌ for no match.  
Suggested Improvement: Provide specific recommendations for skills enhancement.  
Example Table Format:  Required Skill	Candidate's Resume	Match	Suggested Improvement Python	Yes	✅	Emphasize Python-related tasks, 
like data processing or machine learning, in more detail. 
SQL	Yes	✅	Highlight complex query-writing experience and mention tools like SQL Server or Snowflake if applicable. 
CI/CD	No	❌	Gain experience in CI/CD pipelines by building personal projects or training on tools like Jenkins or Azure. 
Experience Enhancement Suggestions Provide bullet points with recommendations for:  Quantifying achievements with specific metrics or impacts.  
Highlighting relevant projects, keywords, or technical achievements.  
Addressing missing skills or gaps with actionable suggestions.  
Optional Revised Resume Entry Write one or two example resume entries that align with the job description while showcasing relevant skills, 
experiences, and measurable outcomes. add one more column for section of skill with group format.  
NOTE: sort according to  section then Match.
"""

input_prompt6 = r"""
make this resume good fit according to jd by adding required skills and experience data engineer role in same latex code format with below format :
\documentclass[letterpaper,11pt]{article}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-0.5in}
\addtolength{\textheight}{1.0in}
\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{ }{0em}{ }[\color{black}\titlerule\vspace{-5pt}]

\pdfgentounicode=1

\newcommand{\resumeItem}[1]{%
  \item\small{#1 \vspace{-2pt}}
}
\newcommand{\resumeSubheading}[4]{%
  \vspace{-2pt}\item
  \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
    \textbf{#1} & #2 \\
    \textit{\small#3} & \textit{\small #4} \\
  \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]} 
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape [Candidate Name]} \\ \vspace{1pt}
    \small [Phone Number] $|$ \href{mailto:[Email Address]}{[Email Address]} $|$ \href{[LinkedIn URL]}{\bf LinkedIn}
\end{center}

\section{Profile}
\begin{itemize}[leftmargin=0.15in, label={}]
  \item [Insert a concise professional summary here.]
\end{itemize}

\section{Technical Skills}
\begin{tabularx}{\textwidth}{@{}l c X@{}}
\textbf{Programming Languages}    & \hspace{0.2cm}: \hspace{0.2cm} &  [Languages] \\
\textbf{Database Management}      & \hspace{0.2cm}: \hspace{0.2cm} &  [Databases] \\
\textbf{Cloud Computing}          & \hspace{0.2cm}: \hspace{0.2cm} &  [Cloud Services] \\
\textbf{Others}                   & \hspace{0.2cm}: \hspace{0.2cm} &  [Other Skills]
\end{tabularx}

\section{Experience}
\resumeSubHeadingListStart
  \resumeSubheading
      {[Company Name]}{[Dates]}
      {[Job Title]}{[Location]}
  \resumeItemListStart
    \resumeItem{[Job responsibility or achievement 1]}
    \resumeItem{[Job responsibility or achievement 2]}
  \resumeItemListEnd
\resumeSubHeadingListEnd

\section{Achievements}
\resumeSubHeadingListStart
  \resumeSubheading
      {[Achievement Title]}{} 
      {[Description]}{}
\resumeSubHeadingListEnd

\section{Certifications}
\begin{itemize}
  \setlength\itemsep{-0.2em}
  \small
  \item [Certification 1]
  \item [Certification 2]
\end{itemize}

\section{Education}
\resumeSubheading
      {[Institution Name]}{[Location]}
      {[Degree, Major]}{[Dates]}

\end{document}
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt5, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt6, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

        # Generate files when the button is clicked
if st.button("Generate Word & PDF"):
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        latex_code = get_gemini_response(input_prompt6, pdf_content, input_text)    
        st.subheader("The latex is")
        st.write(latex_code)
        pdf_file = generate_pdf(latex_code)
        docx_file = generate_word(latex_code)

        # if pdf_file and os.path.exists(pdf_file):
        #     with open(pdf_file, "rb") as file:
        #         st.download_button("Download PDF", file, file_name="output.pdf", mime="application/pdf")

        # if docx_file and os.path.exists(docx_file):
        #     with open(docx_file, "rb") as file:
        #         st.download_button("Download Word", file, file_name="output.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_promp, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

# footer = """
# ---
# #### Made By [Koushik](https://www.linkedin.com/in/gandikota-sai-koushik/)
# For Queries, Reach out on [LinkedIn](https://www.linkedin.com/in/gandikota-sai-koushik/)  
# *Resume Expert - Making Job Applications Easier*
# """

# st.markdown(footer, unsafe_allow_html=True)