from google.colab import files
import pdfplumber
import spacy
import streamlit as st

# Load the spaCy model (this needs to be done here, not in the function)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def preprocess_text(text):
  doc = nlp(text.lower())
  tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
  return " ".join(tokens)

def extract_skills(text):
  skills = ["python", "machine learning", "communication", "teamwork", "leadership"] # Expanded skills list
  found_skills = [skill for skill in skills if skill in text]
  return found_skills

st.title("Resume Skill Extractor")

uploaded_file = st.file_uploader("Choose a resume (PDF)", type="pdf")

if uploaded_file is not None:
    try:
      resume_text = extract_text_from_pdf(uploaded_file)
      clean_resume_text = preprocess_text(resume_text)
      skills_found = extract_skills(clean_resume_text)

      st.write("Extracted skills:")
      if skills_found:
          for skill in skills_found:
              st.write(f"- {skill}")
      else:
          st.write("No skills found in the provided list.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

