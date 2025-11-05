"""
Minimal Test Suite for Phase 7: Tense Consistency
Ensures main tense-correction logic works correctly.
"""

import pytest
from src.phase7_tense import TenseConsistencyCorrector


@pytest.fixture
def corrector():
    """Initialize corrector once per test."""
    return TenseConsistencyCorrector()


# ----------------------------------------------------------------------
# Core Test Cases
# ----------------------------------------------------------------------

def test_irregular_past_conversion(corrector):
    """'go' → 'went' in past context"""
    result = corrector.correct("I go to school yesterday.")
    corrected = result["corrected_text"].strip()
    assert "went" in corrected, f"Expected 'went', got: {corrected}"


def test_irregular_present_conversion(corrector):
    """'went' → 'goes' when habitual context"""
    result = corrector.correct("She went to park every day.")
    corrected = result["corrected_text"].strip()
    assert "goes" in corrected, f"Expected 'goes', got: {corrected}"


def test_future_consistency(corrector):
    """Future alignment between clauses"""
    result = corrector.correct("I will go and she went.")
    corrected = result["corrected_text"].strip()
    assert "will" in corrected and "go" in corrected, f"Future mismatch: {corrected}"


def test_negation_handling(corrector):
    """Negation should normalize correctly"""
    result = corrector.correct("He not walked to school yesterday.")
    corrected = result["corrected_text"].strip()
    assert "didn't walk" in corrected or "did not walk" in corrected, f"Negation fix failed: {corrected}"


def test_conditional_clause(corrector):
    """Basic conditional normalization"""
    result = corrector.correct("If rain don't came, we stay home.")
    corrected = result["corrected_text"].strip()
    assert "doesn’t rain" in corrected or "doesn't rain" in corrected, f"Conditional tense failed: {corrected}"


def test_no_overcorrection(corrector):
    """Ensure correct sentences stay unchanged"""
    result = corrector.correct("He is playing football now.")
    corrected = result["corrected_text"].strip()
    assert corrected == "He is playing football now.", f"Over-corrected: {corrected}"
