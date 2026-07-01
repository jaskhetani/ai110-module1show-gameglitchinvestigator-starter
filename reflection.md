# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran `python -m streamlit run app.py`, the game loaded and looked
finished — a title, a difficulty selector, an input box, and Submit/New Game
buttons. But it was unplayable. The "Higher/Lower" hints pointed the wrong
way, the score jumped around unpredictably, and on some attempts I could type
the exact secret (visible in the Developer Debug Info panel) and still not
win. The UI looked production-ready, which made the bugs more confusing.

- List at least two concrete bugs you noticed at the start
  (for example: "the hints were backwards").

1. The hints were backwards — guessing too high told me to go *higher*.
2. On every even-numbered attempt the game secretly converted the secret
   number to a string, so my integer guess never matched and the comparisons
   broke.
3. The score sometimes went *up* after a wrong guess and could go negative.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 80 when secret is 50 | Hint should say "go LOWER" | Said "📈 Go HIGHER!" (backwards) | No error — a logic bug, not a syntax error |
| Any guess on an even attempt (2nd, 4th, ...) | Compare guess to the secret number | `secret = str(...)` made it compare int to string, so a correct guess failed | No crash; comparison silently wrong |
| Wrong guess on an even attempt | Score should drop by a fixed amount | Score sometimes *increased* by 5, and could go negative | No error — flawed `update_score` logic |
| Click "New Game" after winning | Fully reset the board for a fresh round | Kept old score/status and ignored difficulty (always 1–100) | No error — state not reset |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used ChatGPT (GPT-4o) and an in-editor coding assistant to explain the
Streamlit state model, propose fixes, and help brainstorm edge-case tests.

- Give one example of an AI suggestion that was correct (including what the AI
  suggested and how you verified the result).

I pasted the `check_guess` function and asked why the hints felt backwards.
The AI pointed out that `if guess > secret: return "Too High", "Go HIGHER!"`
is self-contradictory — if your guess is already too high, you need to go
*lower*. It suggested flipping the message text. I verified this by playing:
after the fix, guessing 80 when the secret was 50 correctly told me to go
LOWER, and every subsequent hint pointed me toward the answer.

- Give one example of an AI suggestion that was incorrect or misleading
  (including what the AI suggested and how you verified the result).

When I asked "why does the secret seem to change every time I submit?", the AI
gave the generic textbook answer: "Streamlit re-runs the whole script on every
interaction, so you must store the secret in `st.session_state`." That was
misleading here, because the code *already* had
`if "secret" not in st.session_state`. The real cause was the line
`secret = str(st.session_state.secret)` on even attempts, which turned the
number into a string so comparisons failed. I verified the AI was wrong by
watching the Developer Debug Info panel: the secret value never actually
changed — only the comparison broke — which proved it was a type bug, not a
state bug. The lesson was that the AI answered a common question pattern
without reading my actual code.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I treated a bug as fixed only when I had both a passing test and matching
behavior in the running game. For logic bugs I wrote or ran a pytest case that
would have failed before the fix; for UI/state bugs I reproduced the exact
click sequence in the app and confirmed the new behavior.

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.

I ran `python -m pytest tests/ -v`. The original three `check_guess` tests
initially failed with `NotImplementedError` because the logic still lived in
`app.py`, which showed me the refactor into `logic_utils.py` wasn't done yet.
After moving and fixing the functions, all tests passed (10 passed once I
added edge cases). The edge-case test `test_parse_guess_rejects_decimals`
specifically showed me that my input parser handled `"3.5"` cleanly instead of
silently truncating it.

- Did AI help you design or understand any tests? How?

Yes. I asked the AI to suggest edge cases a number-guessing game should
survive, and it proposed non-numeric input, empty/whitespace input, decimals,
and negative numbers. I turned each into a pytest case, then checked that my
`parse_guess` behavior matched what I actually wanted (for example, I chose to
*reject* decimals rather than truncate them, which differed from the AI's first
idea).

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who
  has never used Streamlit?

Every time you click a button or type in a box, Streamlit throws away the
whole page and runs your Python file again from the top — like refreshing a
web page. That means any normal variable resets to its starting value on every
click. `st.session_state` is a special dictionary that survives those reruns,
so anything you want to remember between clicks (the secret number, the score,
the guess history) has to live there. Once I understood this, the state bugs
made sense: the secret was correctly stored in session state, but "New Game"
wasn't resetting the *other* session-state values, so old scores and statuses
leaked into the next round.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in
  future labs or projects?

Refactoring logic into small, pure functions (like `logic_utils.py`) so I can
unit-test it without the UI. Being able to run `pytest` and get a green bar
gave me real confidence that a fix worked, instead of just eyeballing the app.

- What is one thing you would do differently next time you work with AI on a
  coding task?

I would give the AI the actual code up front instead of describing the symptom.
The most misleading answer I got was a generic response to a common question
("why does my value reset?") that didn't apply because the AI never saw that
the session-state guard already existed.

- In one or two sentences, describe how this project changed the way you think
  about AI-generated code.

I now treat AI-generated code as a confident first draft, not a finished
product — it looked polished and "production-ready" while being full of subtle
logic bugs. I read every line and back it with a test before I trust it.
