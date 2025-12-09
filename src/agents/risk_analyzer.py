import os
from groq import Groq

# Initialize Groq client
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def analyze_risk(message):
    """
    Agent: Risk Analyzer
    Input: structured data from Document Ingestor
    Output: risk assessment
    """
    structured_data = message.get("structured_data", "")

    prompt = f"""
    You are a compliance officer assessing customer KYC risk.
    Based on the structured data below, classify the customer's risk level as:
    - Low
    - Medium
    - High

    Provide a short, clear explanation for your decision.
    Always return your output in JSON format like:
    {{
        "Risk Level": "Medium",
        "Reason": "Customer has incomplete address details but no sanctions hits."
    }}

    Customer Data:
    {structured_data}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI compliance risk analyzer for KYC evaluation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=200,
        temperature=0.3
    )

    risk_result = response.choices[0].message.content.strip()
    return {"risk_assessment": risk_result}
