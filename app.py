import streamlit as st
import tempfile
import os

from tools.pdf_reader import extract_text_from_pdf
from tools.section_parser import split_into_sections
from agents.agent_loop import run_agent
from tools.summary_formatter import format_discharge_summary


st.set_page_config(
    page_title="Discharge Summary Agent",
    layout="wide"
)

st.title("🏥 Discharge Summary Agent")

st.write(
    "Upload a discharge summary PDF and generate a structured summary."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(uploaded_file.read())

        pdf_path = tmp.name

    if st.button("Generate Summary"):

        with st.spinner("Running agent..."):

            pages = extract_text_from_pdf(pdf_path)

            combined_text = "\n".join(pages)

            sections = split_into_sections(
                combined_text
            )

            summary, trace = run_agent(
                sections
            )

            formatted_summary = (
                format_discharge_summary(
                    summary
                )
            )

        st.success("Extraction Complete")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Agent Trace")

            for step in trace:

                st.json(step)

        with col2:

            st.subheader("Discharge Summary")

            st.text_area(
                "",
                formatted_summary,
                height=700
            )

    os.unlink(pdf_path)