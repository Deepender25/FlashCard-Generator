AI Flashcard Generator (for ShelfEx)
![alt text](https://img.shields.io/badge/Python-3.9%2B-blue.svg)

![alt text](https://img.shields.io/badge/Framework-Streamlit-red.svg)

![alt text](https://img.shields.io/badge/Model-Zephyr--7B-yellow.svg)

![alt text](https://img.shields.io/badge/License-MIT-green.svg)

This project is a lightweight but robust Flashcard Generation Tool built for the ShelfEx Internship Assignment. It leverages the open-source Zephyr-7B-β model via the Hugging Face Inference API to automatically convert educational content into a structured, question-and-answer flashcard format.

(Optional) I highly recommend you record a short 2-minute screen capture and link it here!

🎥 Watch a 2-minute Demo Video Here

Table of Contents
Project Overview

Features

Tech Stack

Setup and Installation

How to Run

Sample Execution

Design Decisions & Prompt Engineering

Project Structure

Future Work

Project Overview
The goal of this tool is to streamline the study process by automating the creation of flashcards from materials like textbook chapters, lecture notes, or articles. A user can simply provide their content via text paste or file upload, and the system uses the Zephyr-7B LLM to intelligently extract key concepts and formulate them into clear, concise flashcards.

The application is built with Streamlit for a simple and intuitive user interface, focusing on core functionality, clean code practices, and robust LLM integration.

Features
Core Features
✅ Multiple Content Inputs: Accepts content via direct text input and file uploads (.txt, .pdf).

✅ LLM-Powered Generation: Uses the Zephyr-7B-β model to generate a user-specified number of flashcards.

✅ Simple & Interactive UI: A clean Streamlit interface for easy interaction and configuration.

✅ Subject-Specific Guidance: Allows users to select a subject to provide context to the LLM for better results.

Bonus Features Implemented
✅ Quizlet Export: Generates a .txt file formatted specifically for Quizlet's import function (tab-separated terms/definitions).

✅ CSV Export: Allows users to download their flashcards in a standard .csv format.

Tech Stack
Language: Python

Framework/UI: Streamlit

LLM Integration: Hugging Face Inference API

Model: HuggingFaceH4/zephyr-7b-beta

PDF & Text Processing: PyMuPDF (fitz)

Core Libraries: requests, pandas, demjson3

Setup and Installation
Follow these steps to set up the project locally.

1. Clone the Repository

git clone https://github.com/[Your-Username]/[Your-Repo-Name].git
cd [Your-Repo-Name]
Use code with caution.
Bash
2. Create and Activate a Virtual Environment

# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
Use code with caution.
Bash
3. Install Dependencies
All required libraries are listed in requirements.txt.

pip install -r requirements.txt
Use code with caution.
Bash
4. Provide API Key
You will need a Hugging Face User Access Token with "write" permissions. You can get one from huggingface.co/settings/tokens.

The application requires the API key to be entered directly into the sidebar of the Streamlit UI.

How to Run
Once the setup is complete, run the Streamlit application from your terminal:

streamlit run app.py
Use code with caution.
Bash
Open your web browser and navigate to the local URL provided (usually http://localhost:8501). Enter your Hugging Face API token in the sidebar, paste or upload your content, and click "Generate Flashcards".

Sample Execution
Here is a sample run using an excerpt from a Wikipedia article on Photosynthesis.

Input Text (snippet):

Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy, through a process that converts carbon dioxide and water into sugars and oxygen. The process is crucial for life on Earth as it provides the oxygen in the atmosphere and the primary source of energy for most ecosystems. It occurs in two stages: the light-dependent reactions and the light-independent reactions (Calvin cycle). The light-dependent reactions, which occur in the thylakoid membranes of chloroplasts, capture energy from sunlight to produce ATP and NADPH. The Calvin cycle, which takes place in the stroma of the chloroplasts, uses this energy to convert CO2 into glucose.
Use code with caution.
Text
Generated Flashcards (UI Screenshot):

(Here, you should take a screenshot of your app showing the generated flashcards and embed it in the README)

![App Screenshot](path/to/your/screenshot.png)
Use code with caution.
Markdown
Generated Quizlet Export (quizlet_import.txt):

What are the two stages of photosynthesis?	The two stages are the light-dependent reactions and the light-independent reactions (Calvin cycle).

Where do the light-dependent reactions occur?	They occur in the thylakoid membranes of chloroplasts.

What is the main purpose of the light-dependent reactions?	To capture energy from sunlight and produce ATP and NADPH.

What is the primary function of the Calvin cycle?	To use the energy from ATP and NADPH to convert CO2 into glucose.

...	...
Use code with caution.
⭐️ Design Decisions & Prompt Engineering ⭐️
This section details the reasoning behind key technical and design choices, particularly regarding the LLM integration.

LLM Choice: Zephyr-7B-β
I chose Zephyr-7B-β because it is a powerful, open-source model fine-tuned for instruction-following and chat. It offers a great balance between performance and accessibility (via the free tier of the Hugging Face API), making it ideal for a prototype. Its specific chat template (<|system|>...) allows for clear role-setting, which is crucial for good results.

Prompt Engineering
The effectiveness of this tool hinges on the LLM prompt. My prompt design in llm_handler_hf.py incorporates several key strategies:

System-level Role-setting: The prompt begins with <|system|> to instruct the model to act as an expert flashcard creator.

Strict Output Formatting: The prompt explicitly commands the model to return only a valid JSON list of objects. This instruction is repeated to minimize conversational filler and simplify parsing.

Dynamic Parameters: The prompt dynamically includes the user's desired num_cards and subject to tailor the generation request.

Clear Delimitation: The user's text is wrapped with --- to clearly separate it from the instructions.

# The core prompt structure sent to the model:
prompt = f"""<|system|>
You are an expert flashcard creator. Your task is to generate exactly {num_cards} question-answer flashcards based on the provided text.
Your entire response MUST be a single, valid JSON list of objects. Each object must have a "question" key and an "answer" key.
Do not add any introduction, explanation, or any text outside of the main JSON list.
Your response must start with '[' and end with ']'.</s>
<|user|>
Generate flashcards for the following text on the subject of '{subject}':
---
{text}
---</s>
<|assistant|>
"""
Use code with caution.
Python
Handling LLM Edge Cases & Robustness
LLM outputs can be unreliable. I implemented several features to make the application more robust:

JSON Sanitizer: Models often return conversational text (e.g., "Here are your flashcards:") before the JSON, or fail to close the final object in a list. The fix_json_format function in llm_handler_hf.py intelligently strips extraneous text and uses regular expressions to detect and fix common formatting errors before parsing.

Lenient JSON Parser: I chose the demjson3 library because it is more tolerant of minor syntax errors (like trailing commas) than the standard json library, further increasing the success rate of parsing the model's output.

Specific Error Handling: The application provides clear, user-friendly error messages for common API issues, such as the 503 Model is loading error from Hugging Face, API timeouts, or JSON decoding failures.

Project Structure
The codebase is organized for modularity and readability.

.
├── app.py              # Main Streamlit application UI and logic
├── llm_handler_hf.py   # Module for all Hugging Face API interactions and prompt logic
├── requirements.txt    # Project dependencies
├── .gitignore          # Git ignore file
├── .env.example        # Example environment variable file
└── README.md           # This file
Use code with caution.
Future Work
This prototype is a solid foundation that could be extended in several ways:

Flashcard Editing: Implement a feature to allow users to review and edit the generated Q&A pairs directly in the UI before exporting.

Advanced Export: Add direct export support for Anki (via genanki) and other popular flashcard platforms.

Difficulty & Grouping: Enhance the prompt to ask the model to assign a difficulty level (Easy, Medium, Hard) and group flashcards by sub-topic.

Deployment: Package the application in a Docker container and deploy it to a service like Streamlit Community Cloud or Hugging Face Spaces for public access.