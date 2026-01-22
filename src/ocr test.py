from PIL import Image

import pytesseract

from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor

from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def ocr_read_document(image_path: str) -> str:
    """Reads an image from the given path and returns extracted text using OCR."""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"Error reading image: {e}"

from IPython.display import display
image_path = 'invoice.png'
img = Image.open(image_path)
display(img)