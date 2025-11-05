# src/utils.py — OFFLINE FOREVER | AUTO SERVER START | FINAL BUILD

import os
import socket
import re
import logging
import urllib.request
import zipfile
import shutil
import nltk
import subprocess
from threading import Lock
from typing import List
import language_tool_python
import spacy
import time

# === SUPPRESS WARNINGS ===
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# === SINGLETONS ===
_nlp = None
_tool = None
_lock = Lock()

# === PATHS ===
LOCAL_DIR = os.path.expanduser(r"~/.languagetool/LanguageTool-6.6")
JAR_PATH = os.path.join(LOCAL_DIR, "languagetool-server.jar")
DOWNLOAD_URL = "https://languagetool.org/download/LanguageTool-6.6.zip"

# === NLTK Setup ===
def _ensure_nltk():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)
_ensure_nltk()

# === CHECK IF PORT IS OPEN ===
def _is_port_open(port=8081):
    """Check if the local LanguageTool server is running."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

# === AUTO START LOCAL SERVER ===
def _start_local_server():
    """Automatically start LanguageTool server if not running."""
    if _is_port_open(8081):
        logger.info("✅ Local LanguageTool server already running on port 8081.")
        return True

    if not os.path.exists(JAR_PATH):
        logger.error(f"❌ Missing JAR file at {JAR_PATH}. Please ensure it's installed.")
        return False

    logger.info("🚀 Starting local LanguageTool server...")
    cmd = f'start /B java -cp "{JAR_PATH}" org.languagetool.server.HTTPServer --port 8081 --allow-origin "*"'
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait until port becomes active
    for _ in range(15):
        if _is_port_open(8081):
            logger.info("✅ LanguageTool server started successfully on port 8081.")
            return True
        time.sleep(1)

    logger.error("❌ Failed to start LanguageTool server automatically.")
    return False

# === VERIFY OR DOWNLOAD LANGUAGE TOOL (One-Time) ===
def _download_lt_once():
    """Ensures LanguageTool JAR exists locally (downloads once if missing)."""
    if os.path.exists(JAR_PATH):
        return

    logger.warning("⚠️ LanguageTool not found — downloading for offline use...")
    os.makedirs(LOCAL_DIR, exist_ok=True)

    try:
        urllib.request.urlretrieve(DOWNLOAD_URL, os.path.join(LOCAL_DIR, "LanguageTool.zip"))
        with zipfile.ZipFile(os.path.join(LOCAL_DIR, "LanguageTool.zip"), "r") as z:
            z.extractall(LOCAL_DIR)
        os.remove(os.path.join(LOCAL_DIR, "LanguageTool.zip"))
        logger.info("✅ LanguageTool downloaded and extracted successfully.")
    except Exception as e:
        raise RuntimeError(f"❌ Could not prepare LanguageTool offline JAR.\nError: {e}")

# === GET LANGUAGE TOOL (OFFLINE ONLY) ===
def get_language_tool() -> language_tool_python.LanguageTool:
    """
    Load LanguageTool in fully offline mode.
    1. Checks if local server is running.
    2. If not, starts it automatically.
    3. Connects locally with language_tool_python.
    """
    global _tool
    with _lock:
        if _tool is not None:
            return _tool

        _download_lt_once()
        if not _is_port_open(8081):
            _start_local_server()

        # Connect strictly to localhost
        _tool = language_tool_python.LanguageTool('en-US', remote_server='http://localhost:8081')
        logger.info("✅ LanguageTool connected (offline, localhost:8081).")
        return _tool

# === LOAD SPACY MODEL (FAST FALLBACK) ===
def get_spacy_model():
    global _nlp
    with _lock:
        if _nlp is not None:
            return _nlp

        try:
            _nlp = spacy.load("en_core_web_trf", disable=["ner", "textcat"])
            logger.info("✅ spaCy transformer model loaded (en_core_web_trf).")
        except OSError:
            logger.warning("⚠️ Transformer model not found → using en_core_web_sm.")
            _nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
        return _nlp

# === TEXT UTILITIES ===
def preprocess_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())

def get_sentences(text: str) -> List[str]:
    doc = get_spacy_model()(text)
    return [s.text.strip() for s in doc.sents if s.text.strip()]

# === PRINT HELPERS ===
def print_phase_header(phase: int, title: str):
    print("\n" + "=" * 60)
    print(f"  PHASE {phase}: {title}")
    print("=" * 60)

def print_correction(before: str, after: str, msg: str = ""):
    if before != after:
        print(f"   {msg}")
        print(f"   BEFORE: {before}")
        print(f"   AFTER:  {after}")
        print("   " + "-" * 50)

# === BLEU SCORE ===
def compute_bleu(reference: str, candidate: str) -> float:
    from nltk.translate.bleu_score import sentence_bleu
    from nltk.tokenize import word_tokenize
    ref = word_tokenize(reference.lower())
    cand = word_tokenize(candidate.lower())
    return sentence_bleu([ref], cand, weights=(0.5, 0.5)) if ref and cand else 0.0
