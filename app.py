import streamlit as st
import pandas as pd
from enrich import enrich_companies

st.title("🧠 AI Lead Enrichment Tool")

uploaded_file = st.file_uploader("📄 Upload CSV with `company` column", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Validate input
        if 'company' not in df.columns:
            st.error("❌ CSV must contain a column named 'company'.")
        else:
            st.success("✅ File uploaded successfully!")

            if st.button("🚀 Run Enrichment"):
                st.info("Running enrichment... Please wait ⏳")

                company_list = df['company'].dropna().tolist()
                result_df = enrich_companies(company_list)

                # Show preview
                st.subheader("📊 Enriched Results")
                st.dataframe(result_df)

                # Save to CSV for download
                output_path = "enriched_output.csv"
                result_df.to_csv(output_path, index=False)

                with open(output_path, "rb") as f:
                    st.download_button("📥 Download Output CSV", f, file_name="enriched_output.csv")

    except Exception as e:
        st.error(f"⚠️ Error reading CSV: {e}")
