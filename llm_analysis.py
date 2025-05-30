import os
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

def analyze_with_llm(homepage_text, company_name):
    prompt = f"""
You are a B2B AI expert helping a lead generation company understand its prospects.

Here's some text from {company_name}'s homepage:
\"\"\"{homepage_text}\"\"\"

1. Summarize what this company does.
2. Who is their likely target customer?
3. Suggest a custom AI automation idea that QF Innovate could pitch to them.
"""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return {
            "summary_from_llm": response.text.split("\n")[0],
            "automation_pitch_from_llm": "\n".join(response.text.split("\n")[1:])
        }
    except Exception as e:
        return {"summary_from_llm": "", "automation_pitch_from_llm": ""}
