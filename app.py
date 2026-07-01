import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    hint_message,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("A number-guessing game — now de-glitched.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def start_new_round(reset_high_score=False):
    """Reset all per-round state using the current difficulty range."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    if reset_high_score:
        st.session_state.high_score = 0


# Initialise session state on first load. New Game reuses start_new_round().
if "secret" not in st.session_state:
    start_new_round()

# High score persists across rounds (Stretch: High Score tracker).
if "high_score" not in st.session_state:
    st.session_state.high_score = 0

st.subheader("Make a guess")

# These placeholders are created here (top of the page) but filled in *after*
# the guess is processed, via render_status(). Streamlit reruns the whole
# script top-to-bottom on every click, so writing the score/attempts here
# directly would show the values from *before* the current guess (a
# one-guess-behind lag). Filling placeholders after processing fixes that.
info_box = st.empty()

# High score banner (Stretch: High Score tracker / Enhanced UI).
hs_col, score_col = st.columns(2)
hs_metric = hs_col.empty()
score_metric = score_col.empty()

debug_box = st.expander("Developer Debug Info")


def render_status():
    """Fill the status placeholders with the *current* session state.

    Called after a guess is processed (and on the game-over screen) so the
    displayed score, high score, and attempts-left always reflect the latest
    guess rather than the previous one.
    """
    attempts_left = attempt_limit - st.session_state.attempts
    info_box.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left}"
    )
    hs_metric.metric("🏆 High Score", st.session_state.high_score)
    score_metric.metric("⭐ Current Score", st.session_state.score)
    with debug_box:
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_round()
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_status()
    st.stop()


def hot_or_cold(distance, span):
    """Return an emoji 'temperature' for how close a guess is (Enhanced UI)."""
    ratio = distance / span if span else 0
    if distance == 0:
        return "🎯 Bullseye!"
    if ratio <= 0.05:
        return "🔥 Burning hot"
    if ratio <= 0.15:
        return "🌡️ Warm"
    if ratio <= 0.35:
        return "❄️ Cold"
    return "🧊 Freezing"


if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        # Only a valid guess counts as an attempt.
        st.session_state.attempts += 1

        secret = st.session_state.secret
        outcome = check_guess(guess_int, secret)

        if show_hint:
            st.warning(hint_message(outcome))
            if outcome != "Win":
                st.caption(
                    hot_or_cold(abs(guess_int - secret), high - low)
                )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        # Record this guess for the session summary table.
        st.session_state.history.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Result": outcome,
                "Score": st.session_state.score,
            }
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.session_state.high_score = max(
                st.session_state.high_score, st.session_state.score
            )
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

# Refresh the status widgets so score / high score / attempts-left reflect
# the guess that was just processed (not the previous one).
render_status()

# Session summary table (Enhanced UI / Guess History).
if st.session_state.history:
    st.subheader("📜 Guess History")
    st.table(st.session_state.history)

st.divider()
st.caption("Debugged by a human who reads the code. 🕵️")
