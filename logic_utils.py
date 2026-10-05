def get_range_for_difficulty(difficulty: str):  #FIX: Refactored logic into logic_utils.py using agent mode
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50  #FIX: Normal range corrected so Normal has the smaller range, myself
    if difficulty == "Hard":
        return 1, 100  #FIX: Hard range corrected so Hard has the larger range, myself
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):  #FIX: Refactored into logic_utils.py and added low/high range parameters using agent mode
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    if "." in raw:  #FIX: Reject decimals like 17.5 instead of silently truncating to 17, myself
        return False, None, "Enter a whole number."

    try:
        value = int(raw)  #FIX: Parse as int only, so "1e2" and other float forms are no longer accepted, using agent mode
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:  #FIX: Reject out-of-range guesses so they are not accepted as valid, using agent mode
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):  #FIX: Refactored logic into logic_utils.py using agent mode
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:  #FIX: Removed the string-comparison fallback; secret is always an int now, using agent mode
        return "Too High", "📈 Go LOWER!"
    else:
        return "Too Low", "📉 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):  #FIX: Refactored logic into logic_utils.py using agent mode
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number  #FIX: Removed the off-by-one (+1) so a first-try win scores 90, using agent mode
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):  #FIX: Merged duplicate branches; wrong guesses no longer reward points, using agent mode
        return current_score - 5

    return current_score
