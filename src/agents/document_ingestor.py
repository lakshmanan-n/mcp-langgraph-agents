import os
from groq import Groq

# Load API key from environment
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set. "
        "Please export GROQ_API_KEY before running this script."
    )

# Initialize Groq client
client = Groq(api_key=API_KEY)


def process_document(message):
    document_text = message.get("document_text", "")

    prompt = f"""
    Extract the following fields from the document:
    - Customer Name
    - Date of Birth
    - Address
    Return the output strictly in valid JSON format.

    Document:
    {document_text}
    """

    # Use chat.completions (correct Groq API)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent KYC document parser that returns structured JSON output."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300,
        temperature=0.2
    )

    structured_data = response.choices[0].message.content.strip()
    return {"structured_data": structured_data}
