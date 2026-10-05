import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score  #FIX: Imported refactored logic from logic_utils.py using agent mode


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 8,
    "Normal": 5,
    "Hard": 4,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_id" not in st.session_state:  #FIX: Added game_id so New Game / difficulty change can clear the guess box, using agent mode
    st.session_state.game_id = 0

if st.session_state.get("last_difficulty") != difficulty:  #FIX: Regenerate the secret when difficulty changes, using agent mode
    if "last_difficulty" in st.session_state:
        st.session_state.secret = random.randint(low, high)
        st.session_state.attempts = 0  #FIX: Reset attempts on difficulty change so the game is not stuck, using agent mode
        st.session_state.score = 0  #FIX: Reset score on difficulty change, using agent mode
        st.session_state.status = "playing"  #FIX: Reset status on difficulty change so a finished game does not block the new one, using agent mode
        st.session_state.history = []  #FIX: Reset history on difficulty change, using agent mode
        st.session_state.game_id += 1
    st.session_state.last_difficulty = difficulty

st.subheader("Make a guess")

info_placeholder = st.empty()  #FIX: Placeholders so attempts/history update in the same run as the hint, using agent mode
debug_placeholder = st.empty()


def render_status():  #FIX: Draw attempts left and debug history after the guess is processed, using agent mode
    info_placeholder.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )

    with debug_placeholder.container():
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.game_id}"  #FIX: game_id in the key gives a fresh empty input on New Game, using agent mode
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0  #FIX: New Game now resets score, using agent mode
    st.session_state.status = "playing"  #FIX: New Game now resets status, using agent mode
    st.session_state.history = []  #FIX: New Game now resets history, using agent mode
    st.session_state.secret = random.randint(low, high)  #FIX: New secret uses the current difficulty's range, using agent mode
    st.session_state.game_id += 1
    st.rerun()

render_status()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)  #FIX: Validate (incl. range) before counting an attempt, using agent mode

    if not ok:
        st.error(err)  #FIX: Invalid input no longer uses an attempt or enters the history, using agent mode
    else:
        st.session_state.attempts += 1  #FIX: Only valid guesses count as attempts, so the loss check always runs, using agent mode
        st.session_state.history.append(guess_int)
        secret = st.session_state.secret  #FIX: Always pass the secret as an int (removed even-attempt str conversion), using agent mode
        outcome, message = check_guess(guess_int, secret)

        out_of_attempts = (
            outcome != "Win" and st.session_state.attempts >= attempt_limit
        )
        if show_hint and not out_of_attempts:  #FIX: No higher/lower hint on the final wrong attempt, using agent mode
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

    render_status()  #FIX: Refresh attempts left and history immediately after the guess, using agent mode

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
