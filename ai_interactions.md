# AI Interactions Log

> **Stretch features.** Records the AI-assisted work for the stretch
> challenges attempted on this project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent to make multi-step changes
> autonomously.

**What task did you give the agent?**

Refactor the four game functions out of `app.py` into `logic_utils.py`, fix
the starter bugs without breaking the existing pytest suite, then add a
persistent **High Score tracker** and a **Guess History** summary table to
the game.

**What did the agent do?**

- Files modified: `logic_utils.py`, `app.py`, `tests/test_game_logic.py`.
- Implemented all four functions in `logic_utils.py` (previously raising
  `NotImplementedError`) and split the old `(outcome, message)` return of
  `check_guess` into `check_guess` (returns the outcome string the tests
  expect) plus a new `hint_message()` helper.
- In `app.py`: removed the duplicated inline logic, imported from
  `logic_utils`, added a `start_new_round()` helper so "New Game" fully
  resets state, added `high_score` to session state with `st.metric`
  banners, and appended each guess to a `history` list rendered as a table.
- Ran `pytest` (10 passed) and `pycodestyle` (no issues) to verify.

**What did you have to verify or fix manually?**

- I confirmed by hand that the **High Score persists across "New Game"** —
  it does, because `start_new_round()` intentionally does *not* clear
  `st.session_state.high_score` unless `reset_high_score=True` is passed.
- The agent's first version of `check_guess` returned a `(outcome, message)`
  tuple, which broke the existing pytest assertion `result == "Win"`. I had it
  split the message into a separate `hint_message()` helper so the tests pass.
- I tuned the Hot/Cold thresholds (`0.05 / 0.15 / 0.35` of the range) after
  playing a few rounds so "🔥 Burning hot" only shows when you are genuinely
  close.
- **Found a display bug in the agent's UI code:** the "Current Score" and
  "Attempts left" widgets lagged one guess behind, because they were drawn at
  the top of the script *before* the guess was processed lower down (Streamlit
  reruns top-to-bottom). I fixed it by drawing them into `st.empty()`
  placeholders that a `render_status()` helper fills *after* the guess is
  handled. A first attempt at that fix crashed with
  `StreamlitAPIException: Cannot replace a single element with multiple
  elements` because I called `.write()` with multiple arguments on the
  expander container; I corrected it to use a `with debug_box:` block. I
  verified the fix by executing the app end-to-end with Streamlit's `AppTest`
  harness (load, wrong guess, winning guess, and game-over screen all run
  without error and the score updates in the same run).

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Non-numeric input | "Write a pytest case proving parse_guess rejects letters without crashing" | `test_parse_guess_rejects_non_numeric` | ✅ Yes | A guessing game must never crash on typos; it should return a friendly error tuple instead of raising. |
| Empty / whitespace / None | "Add a test covering empty string, spaces, and None for parse_guess" | `test_parse_guess_handles_empty_and_whitespace` | ✅ Yes | Players click Submit with an empty box constantly; all three "no input" cases should behave identically. |
| Decimal input | "Test that '3.5' is rejected as not a whole number" | `test_parse_guess_rejects_decimals` | ✅ Yes | Silently truncating 3.5 → 3 would hide what number was actually used; explicit rejection is clearer. |
| Negative number | "Test parse_guess accepts a negative integer like -7" | `test_parse_guess_accepts_negative_numbers` | ✅ Yes | Parsing and range-checking are separate concerns; `-7` should parse cleanly even if it's out of range. |
| Score floor | "Test that update_score never returns a negative score" | `test_score_never_goes_negative` | ✅ Yes | The starter score logic could go negative; clamping at 0 is the fixed behavior. |
| Consistent penalty | "Test Too High and Too Low cost the same regardless of attempt number" | `test_wrong_guess_penalty_is_consistent` | ✅ Yes | The starter gave a `+5` bonus on some wrong guesses; every wrong guess should cost the same. |
| Unknown difficulty | "Test get_range_for_difficulty falls back to Normal on a bad key" | `test_unknown_difficulty_falls_back_to_normal` | ✅ Yes | An unexpected difficulty string should not crash; it should default to the Normal range. |

**Terminal output (all tests passing):**

```
$ python -m pytest tests/ -v
============================= test session starts =============================
collected 10 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 10%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 20%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 30%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric PASSED    [ 40%]
tests/test_game_logic.py::test_parse_guess_handles_empty_and_whitespace PASSED [ 50%]
tests/test_game_logic.py::test_parse_guess_rejects_decimals PASSED       [ 60%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_numbers PASSED [ 70%]
tests/test_game_logic.py::test_score_never_goes_negative PASSED          [ 80%]
tests/test_game_logic.py::test_wrong_guess_penalty_is_consistent PASSED  [ 90%]
tests/test_game_logic.py::test_unknown_difficulty_falls_back_to_normal PASSED [100%]

============================= 10 passed in 0.23s ==============================
```

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Add professional docstrings to every function in logic_utils.py and make
both files PEP 8 compliant. Run pycodestyle and fix any reported issues.
```

**Linting output (after applying changes):**

```
$ python -m pycodestyle --max-line-length=100 app.py logic_utils.py tests/test_game_logic.py
(no output — 0 style issues)
```

**Changes applied:**

- Added Google-style docstrings (Args/Returns) to all five functions in
  `logic_utils.py`, plus a module docstring explaining why the logic lives
  separately from Streamlit.
- Standardized imports (one per line, alphabetized in `app.py`), kept lines
  under 100 chars, and used blank-line spacing consistent with PEP 8.

<!-- Optional (your words): note which AI naming suggestions you accepted
     or rejected. -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

I pasted the buggy `update_score` function below and asked both models:
"This function sometimes adds points for a wrong guess and lets the score go
negative. Explain the bug and rewrite it so a wrong guess always costs the same
and the score never drops below zero."

```python
def update_score(current_score, outcome, attempt_number):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5   # <-- adds points for a wrong guess
        return current_score - 5
    if outcome == "Too Low":
        return current_score - 5
    return current_score
```

| | Model A | Model B |
|-|---------|---------|
| **Model name** | ChatGPT (GPT-4o) | Gemini |
| **Response summary** | Identified that the `Too High` branch adds `+5` on even attempts and that nothing clamps the score. Rewrote it to a single wrong-guess penalty using `max(0, current_score - 5)`. | Also spotted the `+5` bug and the missing floor, but wrapped the fix in extra `if/elif` branches for `Too High` and `Too Low` that did the same thing, and added a comment suggesting a configurable penalty constant. |
| **More Pythonic?** | ✅ Used `max(0, ...)` to clamp in one line and collapsed both wrong outcomes into one return — concise and readable. | Correct but more verbose; kept separate branches that duplicated the same `-5` logic. |
| **Clearer explanation?** | Explained *why* the even-attempt bonus was a bug in one sentence. | Slightly longer; the extra "configurable constant" idea was useful but not essential and made the core fix harder to see. |

**Which did you prefer and why?**

I preferred ChatGPT's answer and used its `max(0, current_score - 5)` approach
in `logic_utils.py`. It was the more Pythonic fix — collapsing both wrong
outcomes into a single return and clamping in one expression — and its
explanation got to the point faster. Gemini's answer was also correct and its
"configurable penalty constant" idea was a nice thought, but the extra branches
duplicated logic and made the fix look bigger than it needed to be.
