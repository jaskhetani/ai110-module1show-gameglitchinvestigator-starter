# Difficulty -> (low, high) inclusive bounds for the secret number.
# Harder difficulties use a wider range, so "Hard" must be larger than
# "Normal" (the starter code had Hard smaller than Normal, which was a bug).
DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 200),
}


def get_range_for_difficulty(difficulty):
    """Return (low, high) inclusive range for a given difficulty."""
    return DIFFICULTY_RANGES.get(difficulty, (1, 100))


def parse_guess(raw):
    """Parse user input into an int guess.

    Returns: (ok, guess_int, error_message)
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = raw.strip()
    if text == "":
        return False, None, "Enter a guess."

    if "." in text:
        return False, None, "Enter a whole number (no decimals)."

    try:
        value = int(text)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return the outcome string."""
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_message(outcome):
    """Return the hint text for an outcome (direction fixed from starter)."""
    messages = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Too high — go LOWER!",
        "Too Low": "📈 Too low — go HIGHER!",
    }
    return messages.get(outcome, "")


def update_score(current_score, outcome, attempt_number):
    """Update score based on outcome and attempt number (never negative)."""
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    return max(0, current_score - 5)
