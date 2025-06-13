# 🧠 AI Flashcard Generator

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/Model-Zephyr--7B-yellow.svg)](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> 📘 A lightweight, LLM-powered tool to convert educational content into flashcards in seconds.

---

## 🎥 Demo Video

https://github.com/user-attachments/assets/68797cdd-d19b-4feb-b56e-68f8b4c42bf2

---
## 🖼️ Screenshots

![Screenshot 2025-06-13 205813](https://github.com/user-attachments/assets/0357900f-d342-44ee-979b-20c37ff7c5eb)

![Screenshot 2025-06-13 205848](https://github.com/user-attachments/assets/21a2d285-03c4-44a3-a670-3112ec308626)

![Screenshot 2025-06-13 205853](https://github.com/user-attachments/assets/405fff55-8570-477f-a48d-6e60ac265512)

---

## 📑 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Sample Execution](#sample-execution)
- [Design Decisions & Prompt Engineering](#design-decisions--prompt-engineering)
- [Project Structure](#project-structure)
- [Future Work](#future-work)

---

## 🚀 Project Overview

This tool streamlines the study process by automatically generating flashcards from educational content such as textbook chapters, lecture notes, or articles.

Built with **Streamlit** and powered by **Zephyr-7B-β** (via Hugging Face), it offers an intuitive UI and delivers clean, structured Q&A flashcards that can be exported to **Quizlet** or **CSV**.

---

## ✅ Features

### 🔹 Core Features

- ✅ **Multiple Content Inputs** – Paste text or upload `.txt` / `.pdf` files.
- ✅ **LLM-Powered Generation** – Generate a custom number of flashcards using Zephyr-7B.
- ✅ **Interactive UI** – Streamlit-based frontend for simplicity and clarity.
- ✅ **Subject-Specific Context** – Optional subject selection improves relevance.

### 🔸 Bonus Features

- ✅ **Quizlet Export** – Download in `.txt` format (tab-separated).
- ✅ **CSV Export** – Download a `.csv` file of generated flashcards.
- ✅ **Robust JSON Parsing** – Handles minor LLM output errors for stable performance.

---

## 🛠️ Tech Stack

| Layer              | Tools / Libraries |
|-------------------|-------------------|
| Language           | Python            |
| UI Framework       | Streamlit         |
| Model              | Zephyr-7B-β via Hugging Face Inference API |
| Text Processing    | PyMuPDF (fitz)    |
| Data Handling      | pandas            |
| JSON Parsing       | demjson3          |
| HTTP Requests      | requests          |

---

## 🧰 Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Deepender25/FlashCard-Generator.git
cd FlashCard-Generator

2. Create and Activate Virtual Environment
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Get Your Hugging Face API Token
Visit huggingface.co/settings/tokens and generate a User Access Token (with read permissions).

You’ll be prompted to paste this token into the Streamlit sidebar during app usage.

▶️ How to Run
streamlit run app.py
Visit the local URL shown (usually http://localhost:8501) to access the app.

🧪 Sample Execution
🔹 Input Text
Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy...

🔹 Sample Flashcards (JSON)
[
  {
    "question": "What are the two stages of photosynthesis?",
    "answer": "The two stages are the light-dependent reactions and the light-independent reactions (Calvin cycle)."
  },
  {
    "question": "Where do the light-dependent reactions occur?",
    "answer": "They occur in the thylakoid membranes of chloroplasts."
  }
]

🔹 Export Files
quizlet_import.txt

Where do the light-dependent reactions occur?	They occur in the thylakoid membranes of chloroplasts.

flashcards.csv
question,answer
Where do the light-dependent reactions occur?,They occur in the thylakoid membranes of chloroplasts.

🧠 Design Decisions & Prompt Engineering
🔸 Why Zephyr-7B-β?
Instruction-tuned for Q&A tasks

Efficient and open-source

Easy integration with Hugging Face Inference API

🔸 Prompt Engineering Strategy
The prompt used in llm_handler_hf.py:
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

🔸 JSON Cleanup Handling
fix_json_format() strips out extra text or missing brackets.

Uses demjson3 for lenient parsing.

Robust error messages for API failures, timeouts, and decoding issues.

.
├── app.py              # Main Streamlit UI
├── llm_handler_hf.py   # Hugging Face API & prompt logic
├── requirements.txt    # Dependency list
├── .gitignore          # Files to ignore in Git
├── .env.example        # Example for API token handling
└── README.md           # You're reading it!

🔮 Future Work
📝 Flashcard Editor – Let users edit flashcards before exporting.

📦 Anki Export – Add .apkg support via genanki.

🧠 Topic Clustering – Group questions by sub-topic or difficulty.

🚀 Public Deployment – Host on Streamlit Cloud or Hugging Face Spaces.

🌐 Multi-language Support – Generate flashcards in different languages.

📄 License
This project is licensed under the MIT License.
