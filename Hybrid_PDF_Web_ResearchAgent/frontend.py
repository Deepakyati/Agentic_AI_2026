import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os
from backend import graph

st.set_page_config(page_title="Hybrid RAG Agent", layout="wide")
st.title(" Hybrid PDF + Web Research Agent")

# Sidebar: File Upload
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    
    processed_docs = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                loader = PyPDFLoader(tmp_file.name)
                processed_docs.extend(loader.load())
            os.unlink(tmp_file.name) # Clean up temp file
        st.success(f"Loaded {len(uploaded_files)} PDF(s)")

# Main Interface
user_query = st.text_input("Ask a question about your documents:", placeholder="What are the key risks mentioned?")

if st.button("Run Research Agent"):
    if not user_query:
        st.error("Please enter a question.")
    else:
        with st.spinner("Agent is analyzing PDFs and searching the web..."):
            inputs = {
                "question": user_query,
                "documents": processed_docs,
                "pdf_context": "",
                "web_context": ""
            }
            result = graph.invoke(inputs)
            
            # Display Results
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(" From PDF")
                st.write(result['pdf_context'][:500] + "...")
            with col2:
                st.subheader(" From Web")
                st.write(result['web_context'][:500] + "...")
            
            st.divider()
            st.subheader(" Final Verified Response")
            st.markdown(result['final_response'])