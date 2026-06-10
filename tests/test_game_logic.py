from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# --- Core check_guess tests (provided in the starter) ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Stretch: advanced edge-case tests for parse_guess ---

def test_parse_guess_rejects_non_numeric():
    # Letters are not a number and must be rejected, not crash.
    ok, value, err = parse_guess("hello")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_handles_empty_and_whitespace():
    # Empty string and whitespace-only input are treated as "no guess".
    for raw in ["", "   ", None]:
        ok, value, err = parse_guess(raw)
        assert ok is False
        assert value is None
        assert err == "Enter a guess."


def test_parse_guess_rejects_decimals():
    # Decimals are rejected so the player knows the exact number used.
    ok, value, err = parse_guess("3.5")
    assert ok is False
    assert value is None
    assert "whole number" in err


def test_parse_guess_accepts_negative_numbers():
    # A negative integer is still a valid parse (range is checked elsewhere).
    ok, value, err = parse_guess("-7")
    assert ok is True
    assert value == -7
    assert err is None


# --- Stretch: edge-case tests for update_score ---

def test_score_never_goes_negative():
    # A wrong guess from a score of 0 must clamp at 0, not go negative.
    assert update_score(0, "Too High", 1) == 0


def test_wrong_guess_penalty_is_consistent():
    # Too High and Too Low cost the same regardless of attempt parity.
    assert update_score(50, "Too High", 2) == 45
    assert update_score(50, "Too Low", 3) == 45


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)
