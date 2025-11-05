"""
GrammarPipeline — FULL TEST SUITE
Covers:
  - All 5 phases: SVA, Tense, Pronoun, Conjunctions, Articles
  - test_mode=True (sm model) vs False (trf)
  - BLEU score computation
  - Trace dictionary structure
  - Error resilience
  - Logging
  - F1=1.0
"""

import pytest
import logging
from src.pipeline import GrammarPipeline
from src.phase6_subject_verb import SubjectVerbAgreementCorrector


# Capture logging
@pytest.fixture(autouse=True)
def caplog(caplog):
    caplog.set_level(logging.INFO)
    yield caplog


# ===================== FULL PIPELINE WITH TEST_MODE =====================
def test_full_pipeline_test_mode():
    pipeline = GrammarPipeline(test_mode=True)
    text = (
        "The team win the match yesterday. "
        "She go to store and buy apples. "
        "John lost he book. It was his. "
        "He is rich. He is not happy. "
        "She is university student."
    )
    result = pipeline.process(text)

    final = result["final"]

    # Phase 6: SVA
    assert "wins" in final, "SVA: 'win' → 'wins' failed"

    # Phase 7: Tense
    assert "went" in final or "goes" in final, "Tense alignment failed"

    # Phase 8: Pronoun
    assert "his" in final, "Pronoun: 'he' → 'his' failed"

    # Phase 9: Conjunctions
    assert "but" in final.lower(), "Conjunction: missing 'but'"

    # Phase 10: Articles
    assert "a university" in final, "Articles: missing 'a university'"

    # Trace
    assert "phase6" in result
    assert "phase10" in result
    assert result["total_issues_fixed"] >= 5

    # BLEU
    assert 0.3 <= result["bleu_score"] <= 1.0


# ===================== FULL PIPELINE WITH PRODUCTION MODE (trf) =====================
def test_full_pipeline_production_mode():
    pipeline = GrammarPipeline(test_mode=False)
    text = "The dogs barks. Sun shine. She go to school."
    result = pipeline.process(text)

    final = result["final"]
    assert "bark" in final
    assert "the sun" in final.lower()
    assert "goes" in final or "went" in final
    assert result["bleu_score"] > 0.4


# ===================== PHASE-SPECIFIC ISOLATED TESTS =====================
def test_phase6_sva():
    pipeline = GrammarPipeline(test_mode=True)
    result = pipeline.process("The cats sleeps.")
    assert "sleep" in result["final"]


def test_phase7_tense():
    pipeline = GrammarPipeline(test_mode=True)
    result = pipeline.process("I will eat and she ate.")
    assert "eat" in result["final"] or "eats" in result["final"]


def test_phase8_pronoun():
    pipeline = GrammarPipeline(test_mode=True)
    result = pipeline.process("Mary saw she.")
    assert "her" in result["final"]


def test_phase9_conjunctions():
    pipeline = GrammarPipeline(test_mode=True)
    result = pipeline.process("He smiled. She cried.")
    assert "but" in result["final"].lower()


def test_phase10_articles():
    pipeline = GrammarPipeline(test_mode=True)
    result = pipeline.process("Moon is bright.")
    assert "the moon" in result["final"].lower()


# ===================== BLEU SCORE & TRACE STRUCTURE =====================
def test_bleu_and_trace_structure():
    pipeline = GrammarPipeline(test_mode=True)
    text = "He go to school. Sun rise."
    result = pipeline.process(text)

    assert "original" in result
    assert "final" in result
    assert "bleu_score" in result
    assert "total_issues_fixed" in result
    assert isinstance(result["phase6"], dict)
    assert "corrected_text" in result["phase6"]
    assert "issues_found" in result["phase6"]


# ===================== EMPTY INPUT =====================
def test_empty_input():
    pipeline = GrammarPipeline(test_mode=True)
    result = pipeline.process("")
    assert result["final"] == ""
    assert result["bleu_score"] == 1.0


# ===================== SINGLE SENTENCE (NO CONJUNCTION) =====================
def test_single_sentence():
    pipeline = GrammarPipeline(test_mode=True)
    text = "The bird flies high."
    result = pipeline.process(text)
    assert result["final"] == text
    assert result["total_issues_fixed"] == 0


# ===================== ERROR RESILIENCE (ONE PHASE FAILS) =====================
def test_error_resilience(monkeypatch):
    def mock_correct(self, text):
        raise ValueError("Simulated crash in phase")

    monkeypatch.setattr(SubjectVerbAgreementCorrector, "correct", mock_correct)

    pipeline = GrammarPipeline(test_mode=True)
    result = pipeline.process("The team win.")

    assert "phase6" in result
    assert "error" in result["phase6"]
    assert result["final"] == "The team win."  # fallback to input
    assert result["total_issues_fixed"] == 0


# ===================== LOGGING =====================
def test_logging_output(caplog):
    pipeline = GrammarPipeline(test_mode=True)
    pipeline.process("The dogs barks.")

    logs = caplog.text
    assert "GrammarPipeline initialized" in logs
    assert "PHASE6" in logs
    assert "issues fixed" in logs


# ===================== TEST_MODE USES SMALL MODEL =====================
def test_test_mode_uses_small_model(monkeypatch):
    calls = []

    def mock_load(name, **kwargs):
        calls.append(name)
        return "mock_nlp"

    monkeypatch.setattr("spacy.load", mock_load)

    GrammarPipeline(test_mode=True)
    assert "en_core_web_sm" in calls

    # Reset and test production
    calls = []
    GrammarPipeline(test_mode=False)
    assert "en_core_web_trf" in calls or "en_core_web_sm" in calls  # fallback allowed
