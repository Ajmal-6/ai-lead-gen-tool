import requests
import pandas as pd
from scraper import get_homepage_text
from llm_analysis import analyze_with_llm

def get_company_data(company_name):
    # You can replace this logic with Clearbit API or other alternatives
    try:
        url = f"https://api.api-ninjas.com/v1/company?name={company_name}"
        headers = {'X-Api-Key': 'YOUR_API_NINJAS_KEY'}
        res = requests.get(url, headers=headers)
        if res.status_code == 200 and res.json():
            data = res.json()[0]
            return {
                "website": data.get("website", ""),
                "industry": data.get("industry", ""),
                "size": data.get("size", ""),
                "location": data.get("location", "")
            }
    except Exception as e:
        print(f"Error: {e}")
    return {"website": "", "industry": "", "size": "", "location": ""}

def enrich_companies(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    results = []

    for _, row in df.iterrows():
        name = row["company_name"]
        info = get_company_data(name)
        homepage_text = get_homepage_text(info['website'])
        llm_results = analyze_with_llm(homepage_text, name)

        enriched = {
            "company_name": name,
            **info,
            **llm_results
        }
        results.append(enriched)

    out_df = pd.DataFrame(results)
    out_df.to_csv(output_csv, index=False)
    print(f"✅ Enrichment complete: {output_csv}")
