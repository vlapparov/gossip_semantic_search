import pytest

from data.dataset_preparation import preprocess_french_text


# Test cases for preprocess_french_text function
@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("C'est un très bon jour!", "cest tres bon jour"),  # test with accents and special characters
        ("Bonjour, tout le monde!", "bonjour tout monde"),  # test with punctuation and stopwords
        ("LA VIE EST BELLE", "vie belle"),  # test with uppercase and stopwords
        ("J'aime les pâtes!", "jaime pates"),  # test with apostrophes and accented characters
        ("À l'école des étoiles.", "a lecole etoiles"),  # test with accented and special characters
        ("  Des   espaces   multiples  ", "espaces multiples"),  # test with multiple spaces
    ],
)
def test_preprocess_french_text(input_text, expected_output):
    assert preprocess_french_text(
        input_text) == expected_output, f"Failed for input: {input_text}. Got: {preprocess_french_text(input_text)}. Expected: {expected_output}"
