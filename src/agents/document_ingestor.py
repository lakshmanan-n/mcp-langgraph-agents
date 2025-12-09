import os
from groq import Groq

# Initialize Groq client
API_KEY = os.environ.get("GROQ_API_KEY")
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

    # Use chat.completions instead of completions
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
