"""Core game logic for the Number Guessing Game.

These functions were refactored out of ``app.py`` so they can be unit
tested independently of Streamlit. Keeping the logic here (pure functions
with no Streamlit calls) is what makes the pytest suite possible.
"""

# Difficulty -> (low, high) inclusive bounds for the secret number.
# Harder difficulties use a wider range, so "Hard" must be larger than
# "Normal" (the starter code had Hard smaller than Normal, which made
# Hard *easier* -- that was a bug).
DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 200),
}


def get_range_for_difficulty(difficulty):
    """Return the inclusive ``(low, high)`` range for a difficulty.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"`` or ``"Hard"``.

    Returns:
        A ``(low, high)`` tuple. Unknown difficulties fall back to the
        ``"Normal"`` range so the game never crashes on bad input.
    """
    return DIFFICULTY_RANGES.get(difficulty, (1, 100))


def parse_guess(raw):
    """Parse raw text input into an integer guess.

    Args:
        raw: The raw string from the text box (may be ``None``).

    Returns:
        A ``(ok, guess_int, error_message)`` tuple. On success ``ok`` is
        ``True``, ``guess_int`` holds the integer and ``error_message`` is
        ``None``. On failure ``ok`` is ``False``, ``guess_int`` is ``None``
        and ``error_message`` explains what went wrong.
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = raw.strip()
    if text == "":
        return False, None, "Enter a guess."

    # Reject decimals explicitly instead of silently truncating them, so
    # the player always knows exactly what number was used.
    if "." in text:
        return False, None, "Enter a whole number (no decimals)."

    try:
        value = int(text)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess to the secret number.

    Args:
        guess: The player's integer guess.
        secret: The secret integer to compare against.

    Returns:
        The outcome as a string: ``"Win"``, ``"Too High"`` or ``"Too Low"``.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_message(outcome):
    """Return the player-facing hint text for an outcome.

    Note the direction: a guess that is *too high* means the player should
    aim **lower** next time. The starter code had these reversed.

    Args:
        outcome: An outcome string from :func:`check_guess`.

    Returns:
        A short, emoji-decorated hint string.
    """
    messages = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Too high — go LOWER!",
        "Too Low": "📈 Too low — go HIGHER!",
    }
    return messages.get(outcome, "")


def update_score(current_score, outcome, attempt_number):
    """Update the running score after a guess.

    A win awards more points the fewer attempts were used. A wrong guess
    costs a small, *consistent* penalty (the starter code sometimes added
    points for a wrong guess). The score never drops below zero.

    Args:
        current_score: The score before this guess.
        outcome: An outcome string from :func:`check_guess`.
        attempt_number: How many guesses have been made this round (1-based).

    Returns:
        The new integer score.
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    # Any wrong guess (Too High or Too Low) costs the same.
    return max(0, current_score - 5)
