"""
Phase 9: Conjunctions & Sentence Flow — CORE TEST SUITE
Covers only essential cases:
  - Contrast: but
  - Cause-Result: so
  - Sequence: then
  - Addition: and
  - Punctuation & correctness
  - No over-insertion
  - Edge case
"""

import pytest
from src.phase9_conjunctions import ConjunctionsCorrector


@pytest.fixture
def corrector():
    """Initialize corrector once per test."""
    return ConjunctionsCorrector()


# ===================== CONTRAST =====================
def test_contrast_but(corrector):
    result = corrector.correct("He is rich. He is not happy.")
    corrected = result["corrected_text"]
    assert "but" in corrected.lower(), f"Should add 'but': {corrected}"


# ===================== CAUSE-RESULT =====================
def test_cause_result_so(corrector):
    result = corrector.correct("It rained heavily. We stayed home.")
    corrected = result["corrected_text"]
    assert "so" in corrected.lower(), f"Should add 'so': {corrected}"


# ===================== SEQUENCE =====================
def test_sequence_then(corrector):
    result = corrector.correct("He woke up. He brushed his teeth.")
    corrected = result["corrected_text"]
    assert "then" in corrected.lower(), f"Should add 'then' for sequence: {corrected}"


# ===================== ADDITION =====================
def test_addition_and(corrector):
    result = corrector.correct("She likes tea. She likes coffee.")
    corrected = result["corrected_text"]
    assert "and" in corrected.lower(), f"Should add 'and': {corrected}"


# ===================== PUNCTUATION & NO OVER-INSERTION =====================
def test_no_change_when_connected(corrector):
    result = corrector.correct("He smiled, but she cried.")
    corrected = result["corrected_text"]
    assert corrected == "He smiled, but she cried.", f"Should not add extra connector: {corrected}"


def test_no_change_single_sentence(corrector):
    result = corrector.correct("The cat sleeps.")
    corrected = result["corrected_text"]
    assert corrected == "The cat sleeps.", f"Should skip single sentence: {corrected}"


# ===================== EDGE CASE =====================
def test_contrast_with_negation(corrector):
    result = corrector.correct("I have money. I not spend it.")
    corrected = result["corrected_text"].lower()
    assert "but" in corrected, f"Should add 'but' for negation contrast: {corrected}"
