"""
Phase 10: Article Usage Correction — CORE TEST SUITE
Covers only essential cases:
  - a/an choice
  - zero article
  - definite article
  - conditional article use
  - correctness (no over-correction)
  - punctuation & capitalization
  - key edge case
"""

import pytest
from src.phase10_articles import ArticleUsageCorrector


@pytest.fixture
def corrector():
    """Initialize corrector once per test."""
    return ArticleUsageCorrector()


# ===================== A / AN CHOICE =====================
def test_an_before_vowel(corrector):
    result = corrector.correct("She is a engineer.")
    corrected = result["corrected_text"]
    assert "an engineer" in corrected, f"Should fix 'a' → 'an': {corrected}"


def test_a_before_consonant_sound(corrector):
    result = corrector.correct("He has an unique idea.")
    corrected = result["corrected_text"]
    assert "a unique" in corrected, f"Should fix 'an' → 'a' for 'unique': {corrected}"


def test_an_hour(corrector):
    result = corrector.correct("It took a hour.")
    corrected = result["corrected_text"]
    assert "an hour" in corrected, f"Should use 'an hour': {corrected}"


# ===================== ZERO ARTICLE =====================
def test_zero_article_school(corrector):
    result = corrector.correct("She goes to a school every day.")
    corrected = result["corrected_text"]
    assert "to school" in corrected, f"Should remove 'a': {corrected}"


def test_zero_article_dinner(corrector):
    result = corrector.correct("We had a dinner at 7.")
    corrected = result["corrected_text"]
    assert "had dinner" in corrected, f"Should remove 'a': {corrected}"


# ===================== DEFINITE ARTICLE (THE) =====================
def test_the_sun(corrector):
    result = corrector.correct("Sun is shining.")
    corrected = result["corrected_text"]
    assert "the sun" in corrected.lower(), f"Should add 'the': {corrected}"


def test_the_internet(corrector):
    result = corrector.correct("I use internet daily.")
    corrected = result["corrected_text"]
    assert "the internet" in corrected.lower(), f"Should add 'the': {corrected}"


# ===================== CONDITIONAL ARTICLE =====================
def test_if_rain(corrector):
    result = corrector.correct("If rain comes, we stay home.")
    corrected = result["corrected_text"]
    assert "the rain" in corrected.lower(), f"Should add 'the': {corrected}"


# ===================== NO OVER-CORRECTION =====================
def test_no_change_when_correct(corrector):
    result = corrector.correct("She is a doctor. He goes to school.")
    corrected = result["corrected_text"]
    assert corrected == "She is a doctor. He goes to school.", f"Should not modify: {corrected}"


# ===================== PUNCTUATION & CAPITALIZATION =====================
def test_spacing_and_capitalization(corrector):
    result = corrector.correct("She is a student , and he is a teacher.")
    corrected = result["corrected_text"]
    assert "student, and" in corrected, f"Should fix spacing: {corrected}"


def test_capitalized_article(corrector):
    result = corrector.correct("A University is big.")
    corrected = result["corrected_text"]
    assert "A university" in corrected, f"Should preserve capitalization: {corrected}"


# ===================== EDGE CASE =====================
def test_acronym_mba(corrector):
    result = corrector.correct("He has a MBA degree.")
    corrected = result["corrected_text"]
    assert "an MBA" in corrected, f"Should use 'an' for acronym: {corrected}"
