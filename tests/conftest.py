"""
Pytest configuration: Preload models + suppress warnings + NLTK setup
Optimized for stable offline testing (lightweight models only).
"""

import pytest
import warnings
import nltk
import os

# ==============================================================
#   IMPORT ONLY WHAT EXISTS
# ==============================================================
from src.utils import get_language_tool, get_spacy_model

# --------------------------------------------------------------
#   OPTIONAL: Stub for Gramformer (required by the fixture below)
# --------------------------------------------------------------
def _get_gramformer_stub():
    """
    Returns a harmless object that mimics the Gramformer API used in tests.
    The real Gramformer is **not needed** for your capstone (you only use LT + spaCy).
    """
    class DummyGramformer:
        def correct(self, text, **kwargs):
            return text  # pass-through – no change
        def __call__(self, text):
            return [(text, 1.0)]  # mimic generate-corrections API
        use_gpu = False
    return DummyGramformer()

# ==============================================================
#   SAFETY + WARNING FILTERS
# ==============================================================
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*use_auth_token.*")
warnings.filterwarnings("ignore", message=".*weights_only.*")
warnings.filterwarnings("ignore", message=".*SwigPyObject.*")
warnings.filterwarnings("ignore", message=".*resume_download.*")

# ==============================================================
#   NLTK DOWNLOADS (safe & silent)
# ==============================================================
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)

# ==============================================================
#   TEST MODE ENV VARIABLE
# ==============================================================
os.environ["TEST_MODE"] = "True"

# ==============================================================
#   FIXTURE: Lightweight spaCy model
# ==============================================================
@pytest.fixture(scope="session")
def nlp():
    """
    Use small spaCy model during tests to prevent memory/RAM crashes.
    Production code still uses 'en_core_web_trf'.
    """
    return get_spacy_model(test_mode=True)

# ==============================================================
#   FIXTURE: Preload Grammar Tools Once
# ==============================================================
@pytest.fixture(scope="session", autouse=True)
def preload_models():
    """Preload LanguageTool + (optional) Gramformer safely in lightweight mode."""
    print("\n[Setup] Preloading lightweight models for tests...")

    # 1. Load LanguageTool offline (no download)
    lt = get_language_tool()
    print("[OK] LanguageTool loaded (offline).")

    # 2. Load **stub** Gramformer – never crashes, never needs GPU
    gf = _get_gramformer_stub()
    print("[OK] Gramformer stub loaded (safe mode).")

    print("[Setup Complete] All models ready for testing.\n")
    return {"tool": lt, "gramformer": gf}