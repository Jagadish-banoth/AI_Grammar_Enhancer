"""
Minimal Test Suite for Phase 8: Pronoun–Antecedent Agreement
Covers only key logic for correctness and stability.
"""

import pytest
from src.phase8_pronoun import PronounAgreementCorrector


@pytest.fixture
def corrector():
    """Initialize corrector once per test."""
    return PronounAgreementCorrector()


# ----------------------------------------------------------------------
# Core Tests
# ----------------------------------------------------------------------

def test_gender_male_agreement(corrector):
    """Ensure 'John' aligns with 'his' not 'him'."""
    result = corrector.correct("John lost him book.")
    corrected = result["corrected_text"].strip()
    assert "his" in corrected, f"Expected 'his', got: {corrected}"


def test_gender_female_agreement(corrector):
    """Ensure 'Mary' aligns with 'her'."""
    result = corrector.correct("Mary saw she in the mirror.")
    corrected = result["corrected_text"].strip()
    assert "her" in corrected, f"Expected 'her', got: {corrected}"


def test_number_plural_agreement(corrector):
    """Plural antecedents → 'their'/'them'."""
    result = corrector.correct("The students forgot he books.")
    corrected = result["corrected_text"].strip()
    assert "their" in corrected, f"Expected 'their', got: {corrected}"


def test_case_nominative_vs_objective(corrector):
    """Fix 'Him went' → 'He went'."""
    result = corrector.correct("Him went to the store.")
    corrected = result["corrected_text"].strip()
    assert "He" in corrected, f"Expected 'He', got: {corrected}"


def test_possessive_correction(corrector):
    """'The cat licked it paw' → 'its paw'."""
    result = corrector.correct("The cat licked it paw.")
    corrected = result["corrected_text"].strip()
    assert "its" in corrected, f"Expected 'its', got: {corrected}"


def test_no_overcorrection(corrector):
    """Ensure correct sentences remain unchanged."""
    result = corrector.correct("She gave him her book. It was theirs.")
    corrected = result["corrected_text"].strip()
    assert corrected == "She gave him her book. It was theirs.", f"Over-corrected: {corrected}"
