# app.py
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from llm_handler_hf import generate_flashcards_hf

# --- NEW: Helper function for Quizlet Formatting ---
def format_for_quizlet(flashcards: list) -> str:
    """
    Formats a list of flashcard dictionaries into a string suitable for Quizlet's import function.
    - Term and Definition are separated by a tab ('\t').
    - Cards are separated by two newlines ('\n\n').
    """
    # We replace any newlines inside the text itself to prevent breaking the format
    quizlet_lines = []
    for card in flashcards:
        question = card.get('question', '').replace('\n', ' ').strip()
        answer = card.get('answer', '').replace('\n', ' ').strip()
        quizlet_lines.append(f"{question}\t{answer}")
    
    return "\n\n".join(quizlet_lines)

# --- UI Configuration ---
st.set_page_config(page_title="ShelfEx Flashcard Generator", page_icon="📚", layout="wide")
st.title("🧠 AI Flashcard Generator (Zephyr-7B)")
st.markdown("This tool uses a free, open-source model ([Zephyr-7B](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)) to generate flashcards from your notes.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Hugging Face API Token:", type="password", help="A 'write' permission token is recommended.")
    if not api_key:
        st.info("Please enter your Hugging Face API Token to begin. You can get one from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).")
        st.stop()
    
    st.header("Options")
    num_cards = st.slider("Number of flashcards to generate:", min_value=5, max_value=25, value=10)
    subject = st.selectbox("Select Subject (optional):", ("General", "Biology", "History", "Computer Science", "Physics"))

# --- Helper function to extract text ---
def extract_text(uploaded_file):
    if uploaded_file is None: return ""
    try:
        if uploaded_file.name.endswith('.pdf'):
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                return "".join(page.get_text() for page in doc)
        elif uploaded_file.name.endswith('.txt'):
            return uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return ""

# --- Main App Logic ---
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []

col1, col2 = st.columns(2)

with col1:
    st.subheader("Provide Your Content")
    tab1, tab2 = st.tabs(["📄 Paste Text", "⬆️ Upload File"])
    with tab1:
        pasted_text = st.text_area("Paste your educational content here:", height=350, key="pasted_text_input", label_visibility="collapsed")
    with tab2:
        uploaded_file = st.file_uploader("Or choose a .txt or .pdf file", type=["txt", "pdf"], label_visibility="collapsed")
        input_from_file = extract_text(uploaded_file) if uploaded_file else ""

final_text = pasted_text if pasted_text.strip() else input_from_file

if st.button("✨ Generate Flashcards", type="primary", use_container_width=True):
    if not final_text.strip():
        st.warning("Please provide some text to generate flashcards from.", icon="⚠️")
    else:
        with st.spinner("Generating flashcards with Zephyr-7B... This may be slow as the model loads. Please wait. 🧠"):
            generated_cards, error_msg = generate_flashcards_hf(api_key, final_text, num_cards, subject)
            
            if error_msg:
                st.error(f"**Error:** {error_msg}", icon="🚨")
                st.session_state.flashcards = []
            elif not generated_cards:
                 st.error("The AI returned no flashcards. Please try a different text.", icon="🚨")
                 st.session_state.flashcards = []
            else:
                st.session_state.flashcards = generated_cards 
                st.success(f"Generated {len(generated_cards)} flashcards successfully!", icon="✅")

# --- Display Flashcards and Export Options in the second column ---
with col2:
    st.subheader("Your Generated Flashcards")
    if not st.session_state.flashcards:
        st.info("Your flashcards will appear here after generation.")
    else:
        # --- NEW: QUIZLET EXPORT BUTTON ---
        quizlet_data = format_for_quizlet(st.session_state.flashcards)
        st.download_button(
            label="📋 Download for Quizlet (.txt)",
            data=quizlet_data,
            file_name='quizlet_import.txt',
            mime='text/plain',
            use_container_width=True,
            help="Copy the text from this file and paste it into Quizlet's 'Import' function."
        )

        # Standard CSV Download Button
        try:
            df = pd.DataFrame(st.session_state.flashcards)
            if 'question' in df.columns and 'answer' in df.columns:
                csv = df[['question', 'answer']].to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download as CSV", csv, f'flashcards.csv', 'text/csv', use_container_width=True)
        except Exception as e:
            st.error(f"Error preparing CSV download: {e}")

        # Display each flashcard
        for i, card in enumerate(st.session_state.flashcards):
            if isinstance(card, dict) and 'question' in card and 'answer' in card:
                with st.expander(f"**Question {i+1}:** {card['question']}"):
                    st.markdown(f"**Answer:** {card['answer']}")
            else:
                st.warning(f"Could not display card {i+1} due to incorrect format.", icon="⚠️")
                st.json(card)