# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|26 guess| expected higher  | got go LOWER    | Comparison error in    |
|        |  when 24 entered.|                 |       check_guess()    |

|Submit G| First attempt    |First attempt not|                        |
         |counted           |counted.         |                        |
         
|Range   |Range according to|Random range when|if new_game(): code     |
          the difficulty    |newgame triggered|   error                |

|Attempts|Easy-8, N-5, H-4  |E-6, N-8, H-5    |

|NewGame |After Game Over   | No change Game  |if new_game() error.    |
         |New Game Button   |
         |Should reset all  |
|Score   |Error in secret   | Changing diffficulty doesnt regenerate secret.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? 

I used Claude Code. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

It accurately identified the error in all of the errors I found myself. 

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.


After the AI listed twelve problems, I only approved fixes for the first five (attempt counting, range check, scoring, difficulty reset). It had also suggested wrapping the input and button in st.form so Enter submits, but I left that out because it was a UI behaviour change outside what I asked for and user could click the submit button anyway. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
When I found the error, I noted it and gave it to the agent. After its "fix", I ran the same error causing input once more. 

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I tested by playing the app in the browser. There turned up a TypeError: parse_guess() takes 1 positional argument but 3 were given, even though the file on disk already had the new signature. Checking the signature from the project's .venv showed the code was correct, and two streamlit run processes were still running. The cause was Streamlit holding the old logic_utils module in memory. Restarting a single Streamlit process fixed it.

- Did AI help you design or understand any tests? How?

Yes. The AI chose the edge-case inputs for the manual check: empty, non-numeric, out-of-range, decimal, exponent and whitespace-padded guesses. It also explained the stale-module TypeError by checking the function's signature from the project's .venv
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button, type in a box or change a dropdown, Streamlit runs your whole Python script again from the top to the bottom. That is a "rerun."

Session state is a fix to that. On each run the script checks if there is already a secret in the session state. If not, it creates one. If so, it reuses it. In this game there werer the secret, attempts, score, status and history in session state.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Pinpoint error locations and then feed it to agent instead of giving agent the whole code to fix. It helps you learn the error. 

- What is one thing you would do differently next time you work with AI on a coding task?

The same thing above. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI is good at finding errors, but it should be given exact context of the way you want the code to behave, not the opposite, so that you can be in loop of what's going on. 
