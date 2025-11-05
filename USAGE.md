# How to Use Grammar Enhancer  
**Phases 6–10 | Full Offline Pipeline**  
**BANOTH JAGADISH** – *AIWAVE X Capstone*

---

## 1. Prerequisites

| Requirement | Command |
|-----------|--------|
| **Python** | `3.9` or higher |
| **pip** | Latest |
| **spaCy Model** | `en_core_web_sm` |

---

## 2. Installation (One-Time)
# Step 1: Clone or extract the project
cd grammar_enhancer

# Step 2: Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate      # For Windows
# source .venv/bin/activate # For macOS/Linux

# Step 3: Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Download required NLP model
python -m spacy download en_core_web_sm

# If you face version conflicts (like tokenizers or transformers), use:

pip install transformers==4.30.1 tokenizers==0.19.1



# Running the Grammar Enhancer
Option 1 — Single Text Run (run.py)
# Use this to test the pipeline on a single example input.
python run.py

Option 2 — Streamlit Web App
# Launch the visual interactive interface.
streamlit run app.py

Option 3 — Full Test Suite (run_all.py)
# Run all correction phases, evaluation metrics (BLEU, F1), and tests automatically.
python run_all.py


