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

<!-- TODO (your words): e.g. confirm the high score persisted across
     New Game, check the Hot/Cold thresholds felt right, etc. -->

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

<!-- TODO (your words): pick ONE bug (e.g. the backwards hint or the
     str(secret) bug), paste it to two different models/tools, and compare.
     This section needs your own hands-on comparison to count. -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
