# 🤖 LLM Tic Tac Toe Battle – Gemma3 vs LLaMA3.2

What happens when two **1B parameter local language models** are dropped into a Tic Tac Toe arena?

🎯 This project is a fun experiment where **Gemma3 (1B)** and **LLaMA3.2 (1B)**, running locally via [Ollama](https://ollama.com), battle it out turn-by-turn using pure language prompts to make their next move.  
No rules hardcoded, no cheat codes — just raw LLM logic trying to win a children's game!
The idea was to understand how does small model with just 1b parameters perform for small tasks like playing Tic-Tac-Toe while runing it on local using Ollama

Let the battle of the billion-parameter bots begin. 🧠⚔️

---

## ⚙️ Installation Guide

### 1. Download Ollama (if you haven’t already)

👉 [https://ollama.com/download](https://ollama.com/download)

This is required to run LLMs locally with minimal setup.

---

### 2. Pull the models using Ollama

```bash
ollama run gemma3:1b
ollama run llama3.2:1b
```

### 3. Clone the repo
We recommend using a virtual environment:
```bash
git clone https://github.com/ameyGujre/LLM-Tic-Tac-Toe-Competition
cd llm-tictactoe-battle
```
Install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Set up your Python environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Run the script
```bash
python llm_tictactoe_battle.py
```


By default, the script is set up to use:

Gemma3 1B as Player X

LLaMA3.2 1B as Player O

You can customize:

Model initialization

Player names

Vector icons (replace 🦙 and 🐐 with your own PNGs)

Just modify the LLM initialization code in the script to match the models you've downloaded via Ollama.

##  🧠 Behind the Scenes

Each move is generated using the LLM's understanding of the current board state, passed in as part of a conversational prompt.
No traditional game engine or AI strategy — just raw language model reasoning.

## 🤔 What Next?
- Add your own models to the mix
- Modify the prompt style or board representation
- Add score tracking, emoji battles, or even a crowd cheer 🤪

## 📩 Suggestions?
Drop a DM: https://www.linkedin.com/in/amey-gujre-400412162/
