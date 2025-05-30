import streamlit as st
from enrich import enrich_companies

st.title("AI Lead Enrichment Tool")

uploaded_file = st.file_uploader("Upload CSV with company_name column", type="csv")

if uploaded_file:
    input_path = "uploaded_input.csv"
    output_path = "enriched_output.csv"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Run Enrichment"):
        enrich_companies(input_path, output_path)
        st.success("Enrichment complete!")
        with open(output_path, "rb") as f:
            st.download_button("Download Output CSV", f, "enriched_output.csv")
