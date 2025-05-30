import requests
import pandas as pd
from scraper import get_homepage_text
from llm_analysis import analyze_with_llm

def get_company_data(company_name):
    try:
        url = f"https://api.api-ninjas.com/v1/company?name={company_name}"
        headers = {'X-Api-Key': 'YOUR_API_NINJAS_KEY'}  # Replace with your real key or load from secrets
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
        print(f"Error fetching data for {company_name}: {e}")
    
    return {"website": "", "industry": "", "size": "", "location": ""}

def enrich_companies(company_list):
    results = []

    for name in company_list:
        try:
            info = get_company_data(name)
            homepage_text = get_homepage_text(info['website'])
            llm_results = analyze_with_llm(homepage_text, name)

            enriched = {
                "company": name,
                **info,
                **llm_results
            }
            results.append(enriched)
        except Exception as e:
            print(f"Error processing {name}: {e}")
            results.append({
                "company": name,
                "website": "",
                "industry": "",
                "size": "",
                "location": "",
                "homepage_text": "",
                "llm_summary": f"Error: {e}"
            })

    return pd.DataFrame(results)
