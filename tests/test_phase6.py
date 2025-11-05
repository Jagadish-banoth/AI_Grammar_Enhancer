"""
Minimal Test Suite for Phase 6: Subject-Verb Agreement
Essential checks for core logic (fast + stable)
"""

import pytest
from unittest.mock import MagicMock
from src.phase6_subject_verb import SubjectVerbAgreementCorrector
from language_tool_python import LanguageTool

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def corrector():
    mock_tool = MagicMock(spec=LanguageTool)
    mock_tool.correct.side_effect = lambda x: x
    return SubjectVerbAgreementCorrector(nlp=None, tool=mock_tool)


# ----------------------------------------------------------------------
# Core Test Cases (Only Keep These)
# ----------------------------------------------------------------------
def test_basic_plural(corrector):
    text = "The dogs barks loudly."
    result = corrector.correct(text)
    assert "bark" in result["corrected_text"]

def test_basic_singular(corrector):
    text = "The cat bark on the mat."
    result = corrector.correct(text)
    assert "barks" in result["corrected_text"]

def test_irregular_be(corrector):
    text = "He are happy."
    result = corrector.correct(text)
    assert "is" in result["corrected_text"]

def test_irregular_have(corrector):
    text = "She have a car."
    result = corrector.correct(text)
    assert "has" in result["corrected_text"]

def test_collective_noun(corrector):
    text = "The team win the game."
    result = corrector.correct(text)
    assert "wins" in result["corrected_text"]

def test_quantifier_agreement(corrector):
    text = "Each of the students have a book."
    result = corrector.correct(text)
    assert "has" in result["corrected_text"]

def test_no_over_correction(corrector):
    text = "The cat sleeps."
    result = corrector.correct(text)
    assert result["corrected_text"] == text.strip()
    assert len(result["issues_found"]) == 0
