# Description:
# This program implements a quiz game named "Braniac." It fetches multiple-choice questions
# from the Open Trivia Database (opentdb.com) using an API. The user selects a quiz topic,
# answers questions and receives a score.
# At the end of the quiz, the user's score is shown, and they have the option to record their score
# on a local leaderboard.

import tkinter as tk       # Import Tkinter for building the GUI and alias it as 'tk' for convenience.
from tkinter import ttk    # Import the themed widget set from Tkinter (ttk) for widgets like Progressbar.
import requests            # Import the requests module to fetch quiz questions via HTTP from an API.
import random              # Import random to randomize question and answer order.
import html                # Import html to unescape HTML entities (e.g., converting &quot; to ").
import os                  # Import os to interact with the operating system (e.g., check if a file exists).

# -----------------------------------------------------------------------------
# Configuration and Global Variables
# -----------------------------------------------------------------------------
# API URL and parameters for fetching quiz questions
TRIVIA_API_BASE_URL = "https://opentdb.com/api.php"
TRIVIA_API_PARAMETERS = {
    "amount": 10,           # Number of questions per quiz
    "difficulty": "medium", # Fixed difficulty level ('easy', 'medium', 'hard')
    "type": "multiple"      # Type of questions (multiple-choice)
}

# Dictionary mapping topic names to their corresponding category IDs in the API.
# "Mixed" means questions from any topic.
TOPICS = {
    "Mixed": None,                # No specific category
    "General Knowledge": 9,
    "Entertainment: Music": 12,
    "Science: Computers": 18,
    "History": 23,
    "Sports": 21,
}

# Global variables to store quiz state
questions = []              # List to store fetched questions
current_question_index = 0  # Index of the current question being shown
score = 0                   # Player's current score
selected_topic = "Mixed"    # Currently selected quiz topic

# -----------------------------------------------------------------------------
# Tkinter Setup
# -----------------------------------------------------------------------------
# Create the main application window
root = tk.Tk()
root.title("Braniac")
root.geometry("800x600")
root.configure(bg="#2C3E50")  # Dark blue-gray background

# Placeholders for dynamically created widgets (set later during execution)
question_label = None         # Label to display the current question text
buttons = []                  # List to hold the answer buttons
score_label = None            # Label to display the player's current score
progress = None               # ttk.Progressbar widget to show quiz progress
progress_counter_label = None # Label to show current question number (e.g., "Question 3 of 10")

# -----------------------------------------------------------------------------
# Leaderboard Helper Functions
# -----------------------------------------------------------------------------
LEADERBOARD_FILE = "leaderboard.txt"  # Local file to record scores

def save_score(name, score):
    """
    Append the player's name and score to the leaderboard file.
    """
    with open(LEADERBOARD_FILE, "a", encoding="utf-8") as file:
        file.write(f"{name},{score}\n")

def show_leaderboard():
    """
    Read the leaderboard from the local file, sort the scores in descending order,
    and display the top 10 scores in a new window.
    """
    scores = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        try:
                            player_score = int(parts[1])
                        except ValueError:
                            player_score = 0
                        scores.append((parts[0], player_score))
    # Sort scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)
    
    leaderboard_frame = tk.Frame(root, bg="#2C3E50")
    leaderboard_frame.pack(fill="both", expand=True)
    
    leaderboard_title = tk.Label(
        leaderboard_frame,
        text="Leaderboard",
        font=("Helvetica", 26, "bold"),
        bg="#2C3E50",
        fg="#F7DC6F"
    )
    leaderboard_title.pack(pady=20)
    
    if scores:  # If there are any recorded scores, display the top 10
        for i, (player, scr) in enumerate(scores[:10], start=1):
            lbl = tk.Label(
                leaderboard_frame,
                text=f"{i}. {player} - {scr}",
                font=("Helvetica", 16),
                bg="#2C3E50",
                fg="#ECF0F1"
            )
            lbl.pack()
    else:
        no_scores_label = tk.Label(
            leaderboard_frame,
            text="No scores yet. Be the first to play!",
            font=("Helvetica", 16),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        no_scores_label.pack(pady=20)
    
    # Button to return to the main menu
    return_button = tk.Button(
        leaderboard_frame,
        text="Return to Main Menu ↩️",
        font=("Arial", 16, "bold"),
        bg="#1ABC9C",
        fg="white",
        activebackground="#16A085",
        activeforeground="white",
        command=welcome_screen
    )
    return_button.pack(pady=20)

# -----------------------------------------------------------------------------
# Quiz Functions
# -----------------------------------------------------------------------------
def fetch_questions():
    """
    Fetch quiz questions from the Open Trivia Database based on the selected topic.
    Returns:
        list: A list of question dictionaries as returned by the API.
    """
    global selected_topic
    TRIVIA_API_PARAMETERS["category"] = TOPICS[selected_topic]
    if selected_topic == "Mixed":
        TRIVIA_API_PARAMETERS.pop("category", None)
    response = requests.get(TRIVIA_API_BASE_URL, params=TRIVIA_API_PARAMETERS)
    data = response.json()
    return data["results"]

def welcome_screen():
    """
    Set up and display the welcome screen. This screen allows the player to select a topic,
    start the quiz, or quit the game.
    """
    global selected_topic
    for widget in root.winfo_children():
        widget.destroy()
    
    # Welcome title
    welcome_label = tk.Label(
        root,
        text="🎉 Welcome to Braniac 🎉",
        font=("Helvetica", 24, "bold"),
        bg="#2C3E50",
        fg="#F7DC6F"
    )
    welcome_label.pack(pady=50)
    
    # Separator text
    separator = tk.Label(
        root,
        text="Select a Topic to Get Started",
        font=("Helvetica", 18, "italic"),
        bg="#2C3E50",
        fg="#EAECEE"
    )
    separator.pack(pady=20)
    
    # Topic selection label and dropdown menu
    topic_label = tk.Label(
        root,
        text="Choose your topic:",
        font=("Helvetica", 16, "bold"),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    topic_label.pack(pady=10)
    
    topic_dropdown = tk.StringVar(root)
    topic_dropdown.set("Mixed")
    topic_menu = tk.OptionMenu(root, topic_dropdown, *TOPICS.keys(), command=select_topic)
    topic_menu.config(font=("Arial", 14), bg="#28B463", fg="white", width=20, height=2)
    topic_menu.pack(pady=20)
    
    # Start Quiz button
    start_button = tk.Button(
        root,
        text="Start Quiz Now 🚀",
        font=("Arial", 16, "bold"),
        bg="#3498DB",
        fg="white",
        activebackground="#2980B9",
        activeforeground="white",
        width=20,
        height=2,
        command=lambda: start_quiz(topic_dropdown.get())
    )
    start_button.pack(pady=30)
    
    # Quit button
    quit_button = tk.Button(
        root,
        text="Quit Game ❌",
        font=("Arial", 16, "bold"),
        bg="#E74C3C",
        fg="white",
        activebackground="#C0392B",
        activeforeground="white",
        width=20,
        height=2,
        command=root.destroy
    )
    quit_button.pack(pady=20)
    
    # Footer text
    footer_label = tk.Label(
        root,
        text="🧠 Let's see how much you know! 🧠",
        font=("Helvetica", 14, "italic"),
        bg="#2C3E50",
        fg="#AAB7B8"
    )
    footer_label.pack(pady=20)

def select_topic(topic):
    """
    Update the selected quiz topic.
    """
    global selected_topic
    selected_topic = topic

def start_quiz(topic):
    """
    Initialize the quiz screen. Fetches the questions, resets the score and counter,
    and sets up the quiz UI which includes the progress bar, current question, answer buttons,
    and an exit option.
    """
    global question_label, buttons, score_label, progress, progress_counter_label
    global questions, current_question_index, score
    current_question_index = 0
    score = 0

    questions = fetch_questions()
    random.shuffle(questions)
    
    # Clear the window before starting the quiz
    for widget in root.winfo_children():
        widget.destroy()
    
    quiz_frame = tk.Frame(root, bg="#2C3E50")
    quiz_frame.pack(fill="both", expand=True)
    
    # Set up the progress bar to show quiz progress
    progress = ttk.Progressbar(quiz_frame, maximum=len(questions), length=600)
    progress.pack(pady=10)
    progress["value"] = 0

    # Progress counter (e.g., "Question 1 of 10")
    progress_counter_label = tk.Label(
        quiz_frame,
        text=f"Question 0 of {len(questions)}",
        font=("Helvetica", 14),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    progress_counter_label.pack(pady=5)
    
    # Label to display the question text
    global question_label
    question_label = tk.Label(
        quiz_frame,
        text="",
        font=("Arial", 18, "bold"),
        bg="#2C3E50",
        fg="#ECF0F1",
        wraplength=600,
        justify="center"
    )
    question_label.pack(pady=20)
    
    # Create answer buttons arranged in a 2x2 grid in a separate frame for better display.
    answers_frame = tk.Frame(quiz_frame, bg="#2C3E50")
    answers_frame.pack(pady=10)
    buttons.clear()
    for row in range(2):
        for col in range(2):
            btn = tk.Button(
                answers_frame,
                text="",
                font=("Arial", 14, "bold"),
                bg="#3498DB",
                fg="white",
                activebackground="#2980B9",
                activeforeground="white",
                width=30, 
                height=3
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            buttons.append(btn)
    
    # Display the current score
    score_label = tk.Label(
        quiz_frame,
        text=f"Score: {score}",
        font=("Helvetica", 14, "bold"),
        bg="#2C3E50",
        fg="#F1C40F"
    )
    score_label.pack(pady=20)
    
    # Button to exit the quiz and return to the welcome screen
    exit_quiz_button = tk.Button(
        quiz_frame,
        text="Exit Quiz",
        font=("Arial", 14, "bold"),
        bg="#E74C3C",
        fg="white",
        activebackground="#C0392B",
        activeforeground="white",
        command=welcome_screen
    )
    exit_quiz_button.pack(pady=10)
    
    update_question()

def update_question():
    """
    Update the quiz screen with the current question, its answer options, and the progress counter.
    If there are no more questions, call the end_screen() function.
    """
    global current_question_index, progress, progress_counter_label
    if current_question_index >= len(questions):
        end_screen()
        return
    
    q = questions[current_question_index]
    # Unescape HTML entities in the question text and set it in the question label.
    question_text = html.unescape(q["question"])
    question_label.config(text=question_text)
    
    # Prepare the answer options, unescape HTML, shuffle them, and assign to answer buttons.
    options = [html.unescape(opt) for opt in q["incorrect_answers"]] + [html.unescape(q["correct_answer"])]
    random.shuffle(options)
    
    for i, option in enumerate(options):
        buttons[i].config(
            text=option,
            command=lambda o=option: check_answer(o, html.unescape(q["correct_answer"]))
        )
    
    # Update the progress bar and counter with the current question number.
    progress["value"] = current_question_index + 1
    progress_counter_label.config(text=f"Question {current_question_index+1} of {len(questions)}")

def check_answer(selected_option, correct_answer):
    """
    Compare the player's selected answer with the correct answer, update the score accordingly,
    and then move to the next question.
    """
    global score, current_question_index
    if selected_option == correct_answer:
        score += 10
    score_label.config(text=f"Score: {score}")
    current_question_index += 1
    update_question()

def end_screen():
    """
    Display the final score and prompt the player to enter their name to record their score on
    the leaderboard. Also offer an option to skip the leaderboard and return to the main menu.
    """
    for widget in root.winfo_children():
        widget.destroy()
    
    end_frame = tk.Frame(root, bg="#2C3E50")
    end_frame.pack(fill="both", expand=True)
    
    end_title = tk.Label(
        end_frame,
        text="Braniac Results 🎉",
        font=("Helvetica", 26, "bold"),
        bg="#2C3E50",
        fg="#F7DC6F"
    )
    end_title.pack(pady=30)
    
    score_display = tk.Label(
        end_frame,
        text=f"Your Final Score: {score}",
        font=("Helvetica", 22, "bold"),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    score_display.pack(pady=20)
    
    # Prompt for the player's name so that their score can be recorded
    name_prompt = tk.Label(
        end_frame,
        text="Enter your name:",
        font=("Helvetica", 16),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    name_prompt.pack(pady=10)
    
    name_entry = tk.Entry(end_frame, font=("Arial", 16), width=20)
    name_entry.pack(pady=10)
    
    submit_button = tk.Button(
        end_frame,
        text="Submit Score",
        font=("Arial", 16, "bold"),
        bg="#1ABC9C",
        fg="white",
        activebackground="#16A085",
        activeforeground="white",
        command=lambda: submit_score(name_entry.get())
    )
    submit_button.pack(pady=20)
    
    skip_button = tk.Button(
        end_frame,
        text="Skip Leaderboard",
        font=("Arial", 16, "bold"),
        bg="#E74C3C",
        fg="white",
        activebackground="#C0392B",
        activeforeground="white",
        command=welcome_screen
    )
    skip_button.pack(pady=10)

def submit_score(name):
    """
    Save the player's score under their provided name and then display the leaderboard.
    If no name is entered, "Anonymous" is used by default.
    """
    if not name.strip():
        name = "Anonymous"
    save_score(name, score)
    show_leaderboard()

# -----------------------------------------------------------------------------
# Start the Application
# -----------------------------------------------------------------------------
welcome_screen()
root.mainloop()
