# Braniac

**Braniac** is a Python-based quiz game that fetches multiple-choice trivia questions from the [Open Trivia Database](https://opentdb.com) API. The game features an interactive graphical user interface built with Tkinter and includes a local leaderboard to track and display high scores.

## Features

- **Dynamic Quiz Questions**  
  Retrieves 10 questions per quiz from the Open Trivia Database, ensuring a new set of multiple-choice trivia each playthrough (no static question set).  

- **Topic Selection**  
  Players can choose a trivia category (e.g., General Knowledge, Music, Computers, History, Sports, or Mixed for a random assortment) before starting the quiz, tailoring the experience to their interests.  

- **Interactive UI Layout**  
  The game uses a Tkinter GUI with a **2×2 grid** of answer buttons, ensuring clear visibility and easy selection.  

- **Progress Tracking**  
  - Displays a **progress bar** and **question counter** to show progress through the quiz (e.g., "Question 3 of 10").  
  - Tracks and updates score in real-time as you answer questions correctly.  

- **Menu and Exit Options**  
  - Quit the quiz anytime and return to the main menu.  
  - Change the topic or start a new session seamlessly.  

- **Local Leaderboard**  
  - High scores are recorded in a local `leaderboard.txt` file.  
  - The game can display the **top 10 scores**, encouraging replayability.  

## Getting Started

### Prerequisites

Ensure you have **Python 3** installed, along with the necessary libraries:

#### Required Python Modules:
- **Tkinter** _(built into Python)_
- **requests** _(for fetching trivia data via API)_
- **random** _(for shuffling questions)_
- **html** _(for processing HTML-encoded text)_
- **os** _(for file handling, leaderboard management)_
- 
To install all required dependencies automatically, run:
  ```bash
  pip install -r requirements.txt

#### Installation

1. **Clone or Download the Project**  
   Run the following command to clone the repository:
   ```bash
   git clone https://github.com/jcmpb2/Braniac.git
2. **Navigate to the Project Directory**
   ```bash
   cd Braniac 
3. **Run the Application**  
   ```bash
   python Braniac.py
