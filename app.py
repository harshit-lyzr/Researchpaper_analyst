from pypdf import PdfReader
from lyzr import Summarizer
import streamlit as st
from PIL import Image
import utils
import os

data = "data"
os.makedirs(data, exist_ok=True)

st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png"
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

st.title("Research Paper Analyst")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("This App uses Lyzr SDK's Summarizer Agent to Summarize Research Paper. You need to just upload Your Research Paper upto 30K Characters and it will summarize your research paper. ")

def style_app():
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)


api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE",type="password")
if api:
    summarizer = Summarizer(api_key=api)
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY Here")

instructions = f"""Summaries this article and follow below instructions:
1/ Ensure that all main points are covered
2/ Give Summaries Topic wise
3/ make bullet points for description
"""

def research_summary():
    uploaded_file = st.file_uploader("Please Upload Your Research Paper", type=['pdf'])
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name} (PDF)")
        file_path = utils.save_uploaded_file(uploaded_file)
        if st.button("Get Summary"):
            if file_path is not None:
                reader = PdfReader(file_path)
                paper = ""
                for i in range(len(reader.pages)):
                    page = reader.pages[i]
                    text = page.extract_text()
                    paper += text

                if len(paper) < 30000:
                    summary = summarizer.summarize(paper, instructions)
                    st.markdown(summary)
                else:
                    st.error("Please Upload Document with only text and have less than 30K Characters")
    else:
        st.warning("Please Upload your Research Paper")

if __name__ == "__main__":
    style_app()
    research_summary()
