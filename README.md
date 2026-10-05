# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.

A Streamlit number-guessing game. Pick a difficulty, guess the secret number within a limited number of attempts, and get higher/lower hints.

- [ ] Detail which bugs you found.

The secret was turned into a string on even attempts, so you couldn't win and the hints were wrong.
Scoring was wrong (wrong guesses could add points, and a first-try win scored 80).
New Game and a difficulty change didn't fully reset the game.
Bad input (empty, non-numeric) used up attempts, and on the last attempt it left the game stuck.
Out-of-range guesses were accepted, and 17.5 silently became 17.
"Attempts left" and the history lagged one guess behind.
Normal and Hard had their ranges reversed.

- [ ] Explain what fixes you applied.

Moved the four functions into logic_utils.py and imported them in app.py.
Always pass the secret as an int.
parse_guess now rejects out-of-range and decimal input, and invalid input no longer counts as an attempt.
Fixed scoring: a first-try win gives 90, and each wrong guess costs 5.
New Game and a difficulty change now reset everything and pick a new secret in the right range.
"Attempts left" and the history now update in the same run as the hint.
Corrected the ranges (Easy 1–20, Normal 1–50, Hard 1–100).

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run streamlit run app.py and pick a difficulty. The sidebar shows the range and attempts allowed.
2. Enter a whole number and click Submit Guess. You get a higher/lower hint, and "Attempts left" and the history update at once.
3. Enter abc, 17.5 or an out-of-range number. You see an error, and no attempt is used.
4. Guess correctly to win (balloons {wohoo} and your score), or run out of attempts to lose.
5. Click New Game or change the difficulty to reset everything with a new secret.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/ -v
collected 3 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 33%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 66%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [100%]

============================== 3 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
