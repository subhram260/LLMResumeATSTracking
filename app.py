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

# submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

# submit3 = st.button("What are the Keywords That are Missing")

# submit4 = st.button("Percentage match")

# submit5 = st.button("Skill Alignment Table Generator")

# submit6 = st.button("LatexResume Generator")

# submit7 = st.button("Interview Q/A Generator")

# submit8 = st.button("Revised Experience Suggestion")

# First row of buttons

button_style = """
<style>
    div[class*="stButton"] > button {
        height: auto; /* Adjusts height automatically */
        width: 100%; /* Makes buttons stretch evenly */
        word-wrap: break-word; /* Ensures long text wraps to the next line */
        text-align: center; /* Centers the text */
        font-size: 14px; /* Set a font size that fits well */
        min-height: 90px; /* Sets a minimum height for uniform-sized boxes */
        max-height: 90px; /* Optional: Prevents oversized buttons */
        padding: 15px; /* Add padding inside the button */
        border: 1px solid white;
    }
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# First row of buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    submit1 = st.button("Tell Me About the Resume")
with col2:
    submit2 = st.button("How Can I Improvise my Skills")
with col3:
    submit3 = st.button("What are the Keywords That are Missing")
with col4:
    submit4 = st.button("Percentage Match")

# Second row of buttons
col5, col6, col7, col8 = st.columns(4)
with col5:
    submit5 = st.button("Skill Alignment Table Generator")
with col6:
    submit6 = st.button("LatexResume Generator")
with col7:
    submit7 = st.button("Interview Q/A Generator")
with col8:
    submit8 = st.button("Revised Experience Suggestion")




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

input_prompt7 = """
You are a highly sophisticated interview strategy consultant, specializing in predicting key interview questions. Your task is to analyze a given resume and job description, then generate a comprehensive and nuanced list of potential interview questions, categorized by typical interview rounds. You must also identify and highlight the most important and frequently asked questions specific to the company and role, based on your analysis. For each question, provide a detailed rationale and a best-answer example based on the resume details.

*Instructions:*

1.  *Comprehensive Analysis:*
    * Perform a deep analysis of the job description, identifying not only explicit requirements but also implied expectations, company culture indicators, and core responsibilities.
    * Analyze the resume with a focus on career trajectory, leadership potential, and strategic thinking, beyond just technical skills.
    * Identify potential gaps or inconsistencies between the resume and job description, noting areas that might trigger probing questions.
    * Pay close attention to the core responsibilities and skills that are repeated or emphasized in the job description as these will be very important.
2.  *Round-Specific Question Generation:*
    * *Screening/Initial Round:* Generate concise, clarifying questions focused on basic qualifications, availability, and initial fit.
    * *Technical/Skills-Based Round:* Produce in-depth technical questions, including scenario-based problems and requests for code/portfolio examples. Include questions that examine problem solving skills.
    * *Behavioral/Competency Round:* Develop STAR method-based questions that delve into leadership, teamwork, conflict resolution, and adaptability, with a focus on past performance predicting future behavior.
    * *Manager/Team Fit Round:* Create questions assessing cultural fit, communication style, and ability to collaborate within a team. Include questions that explore how the candidate would integrate into the team's dynamics.
    * *Executive/Final Round:* Generate strategic, forward-thinking questions that explore the candidate's vision, long-term goals, and ability to contribute to the company's overall success. Include questions that assess the candidates understanding of the company's market position.
3.  *Strategic Question Design:*
    * Incorporate questions that probe the candidate's learning agility, resilience, and ability to handle ambiguity.
    * Design questions that reveal the candidate's motivations, values, and career aspirations.
    * Include questions that explore the candidates ability to learn new skills quickly.
    * Include questions that explore the candidates ability to handle stressful situations.
4.  *Identify Key Questions:*
    * Based on your analysis, highlight the 3-5 most important and likely asked questions, considering the company's priorities and the role's core requirements. Mark these questions with an asterisk (*) or similar indicator.
    * Provide a brief explanation for why these questions are deemed most important.
5.  *Output Format:*
    * Organize questions by interview round, with clear headings for each round.
    * Within each round, include 10-15 realistic interview questions.
    * For each question, provide a detailed rationale, explaining what the interviewer might be trying to assess.
    * For each question also provide a best answer, using the data from the supplied resume.
    * Mark the 3-5 most important questions with an asterisk (*).
    * Provide a summary of why the questions marked with an asterisk are the most important.
    * Use a clear and easy to read format.

 The resume and job description provided
"""

input_prompt8 = """
You are an expert resume editor and career strategist with a deep understanding of Applicant Tracking Systems (ATS) and recruitment best practices. Your task is to perform a granular analysis of ONLY the "Experience" section of the provided resume, comparing it to the given job description to identify gaps, suggest improvements, and provide context-rich sample lines.

The resume and job description provided

Output Format:
Provide separate tables for each gap category identified. Each table should have the following columns:
1. Why This Is Important: This column should provide a compelling explanation of why the skill or experience mentioned in the gap category is important for this specific job, referencing the job description. Quote or paraphrase the relevant requirement from the job description and explain its significance in the context of the role.
2. Resume Evidence (Experience Section): This column should describe in detail what evidence, if any, exists within the provided resume's "Experience" section that relates to the gap category. If there is no direct evidence, state "Not explicitly mentioned" or a similar phrase, but also identify any implied skills or experiences that could be leveraged.
* Note(Strictly): The simple lines should be in a new table after the above 2 columns table.
1. Sample Lines: This column should present context-rich, impactful sample lines addressing the gap. Each sample line should appear in a separate row to ensure clarity. The sample lines should be highly specific, tailored to the resume's existing content and the job description's requirements, using industry-specific keywords, strong action verbs, and quantifiable achievements where possible.
*Detailed Instructions:*

1.  *In-Depth Analysis of Job Description and Resume's Experience Section:* Conduct a thorough and detailed analysis of both the provided job description and ONLY the "Experience" section of the resume. Go beyond surface-level comparisons and focus on identifying nuanced gaps in skills, experience, and how information is presented within the resume's "Experience" section. Consider the context of the job requirements, the candidate's existing experience, and how the "Experience" section can be strategically modified to increase its impact.
2.  *Precise Identification of Gaps in Experience Section:* Focus on identifying key skills and experience requirements from the job description that are missing or not clearly and effectively articulated within the resume's "Experience" section. Prioritize the gaps that are most critical for the job and that can be addressed by rephrasing or adding details to existing experience.
3.  *Structured Output in Separate Tables:* Structure your output as separate tables for each gap category. Use the "Output Format" table structure for each gap category, ensuring each table is self-contained and clearly organized.
4.  *Content of Each Column:*
    * *Why This Is Important:* Provide a detailed and persuasive explanation of why the skill or experience mentioned in the gap category is significant for this specific role. Quote or paraphrase the relevant requirement from the job description and elaborate on its importance, demonstrating an understanding of the employer's needs.
    * *Resume Evidence (Experience Section):* Provide a comprehensive description of what evidence, if any, exists within the provided resume's "Experience" section that relates to the gap category. If there is no direct evidence, state "Not explicitly mentioned" or a similar phrase. However, also analyze the existing content for any implied skills or experiences that could be rephrased or expanded upon to address the gap.
    * *Sample Lines:* Provide 5-6 highly specific, context-rich, and impactful sample lines that could be added to the resume's "Experience" section to address the gap. These lines should be tailored to the candidate's existing experience and the job description's requirements. Use industry-specific keywords, strong action verbs, and quantifiable achievements where possible. The sample lines should demonstrate a clear understanding of how the candidate's experience can be strategically framed to match the job requirements and showcase their qualifications effectively.

Key Improvements and Advanced Elements:
 * Emphasis on Granular Analysis: The prompt stresses a "granular analysis" and going "beyond surface-level comparisons."
 * Focus on Context-Rich Output: The prompt emphasizes providing "context-rich sample lines" and a "detailed and persuasive explanation" of the importance of each gap.
 * ATS and Recruitment Best Practices: The prompt adds the perspective of an expert with "a deep understanding of Applicant Tracking Systems (ATS) and recruitment best practices."
 * Leveraging Implied Skills: The prompt encourages identifying and leveraging "implied skills or experiences" in the resume.
 * Strategic Framing: The prompt focuses on "strategically framed" experience to match job requirements.
 * Quantifiable Achievements: The prompt highlights the importance of using "quantifiable achievements where possible."
 * Clarity on Importance of Sample Lines: The prompt sets a high bar for the sample lines, emphasizing that they should be "highly specific, context-rich, and impactful."
"""


input_prompt6 = r"""
make this resume good fit according to jd by adding required skills and experience for the role in same latex code format with below format :
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

elif submit7:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt7, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")
        # Generate files when the button is clicked


elif submit8:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt8, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")


# if st.button("Generate Word & PDF"):
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         latex_code = get_gemini_response(input_prompt6, pdf_content, input_text)    
#         st.subheader("The latex is")
#         st.write(latex_code)
#         pdf_file = generate_pdf(latex_code)
#         docx_file = generate_word(latex_code)

        # if pdf_file and os.path.exists(pdf_file):
        #     with open(pdf_file, "rb") as file:
        #         st.download_button("Download PDF", file, file_name="output.pdf", mime="application/pdf")

        # if docx_file and os.path.exists(docx_file):
        #     with open(docx_file, "rb") as file:
        #         st.download_button("Download Word", file, file_name="output.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    # else:
    #     st.write("Please upload a PDF file to proceed.")

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