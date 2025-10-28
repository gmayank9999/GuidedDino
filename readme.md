# 🦖 Guided Dino Game (AI-Assisted Chrome Dino Clone)

A modern Python + Pygame recreation of the classic Chrome Dino game — with an **AI "Oracle Agent"** that learns to guide the Dino using rule-based intelligence. The game supports **manual play**, **helper-assisted mode**, and **auto mode** where the AI plays on its own.

---

## 🎯 Problem Statement

Most endless runner games like Chrome Dino are controlled manually, requiring player reflexes to jump and duck over obstacles.  
Our goal is to **introduce an intelligent guide (Oracle Agent)** that can assist or even automate the player's actions by observing the game environment and making decisions — essentially simulating a learning-based helper for gameplay automation.

---

## 🎯 Objectives

- Recreate the Chrome Dino game in **Python using Pygame**.  
- Implement a **helper (oracle) system** that suggests or performs optimal actions (jump/duck).  
- Allow **manual, helper-assisted, and auto** play modes.  
- Design the project for **future reinforcement learning integration** (collecting gameplay data for training).  
- Build a clean, modular folder structure with separate logic for gameplay, helper intelligence, and data collection.

---

## ⚙️ Folder Structure

GuidedDino/
│
├── game.py # Main game file (contains Dino, Obstacle, and game loop)
├── helper.py # Oracle agent logic (rule-based AI)
├── run_collect.py # Collect gameplay data for training
├── data/ # Stores CSV logs of gameplay data
├── assets/ # Optional folder for images/sounds (future use)
└── README.md # Project documentation

---

## 🧠 Flowchart

      ┌──────────────────────────────┐
      │        Start Game            │
      └──────────────┬───────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │  Initialize Dino │
           └──────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │  Spawn Obstacles │
           └──────────────────┘
                     │
                     ▼
           ┌───────────────────────────┐
           │  Check for User Input     │
           │ (Jump / Duck / Toggle AI) │
           └───────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  If Helper/Auto Mode ON    │
        │  → Call Oracle Agent       │
        │  → Decide Jump / Duck      │
        └────────────────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │  Update Dino &   │
           │  Obstacles       │
           └──────────────────┘
                     │
                     ▼
           ┌──────────────────┐
           │ Check Collision  │
           └──────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
 ┌────────────────┐     ┌─────────────────┐
 │ Continue Game   │     │  Game Over      │
 └────────────────┘     └─────────────────┘

---

## 🤖 Expected Solution / Approach

1. **Gameplay Mechanics:**
   - Implement a basic endless runner using `pygame`.
   - The Dino jumps to avoid ground obstacles.

2. **Oracle Agent:**
   - A simple rule-based function analyzes obstacle distance, height, and Dino position.
   - Suggests actions: `jump`, `duck`, or `none`.
   - Acts as an **AI assistant** that can take control automatically in “auto mode”.

3. **Helper & Auto Mode:**
   - Press **`H`** → Toggle Helper (shows AI decisions)
   - Press **`A`** → Toggle Auto Mode (AI plays by itself)
   - Press **`SPACE`** → Jump manually
   - Press **`DOWN`** → Duck manually

4. **Data Collection:**
   - Each frame logs Dino’s state (`distance_to_obstacle`, `obstacle_height`, `speed`, `dino_y`, `action`).
   - Data is saved as `.csv` for future ML model training.

5. **Result:**
   - The Dino can play automatically without collisions.
   - Collected gameplay data can later train a real ML agent.

---

## 🕹️ Controls

| Key | Action |
|-----|---------|
| **SPACE** | Jump |
| **DOWN** | Duck |
| **H** | Toggle Helper Mode |
| **A** | Toggle Auto Mode |
| **ESC / Close Window** | Quit Game |

---

## 💾 Data Collection

To record gameplay data (for ML training):

```bash
python run_collect.py --mode oracle --n 50

🧩 Example State Data (for ML)
| distance_to_obstacle | obstacle_height | speed | dino_y | action |
| -------------------- | --------------- | ----- | ------ | ------ |
| 300                  | 50              | 6     | 250    | jump   |
| 200                  | 70              | 6     | 245    | duck   |
| 100                  | 30              | 6     | 250    | none   |


👨‍💻 Developed With

Language: Python 3.12
Library: Pygame
AI Logic: Rule-based Oracle Agent

📜 License

This project is for educational and research purposes.
Feel free to fork, modify, and build upon it — just give credit ✨

🧠 Author

Mayank Gupta
AI & Game Simulation Project — Guided Dino (2025)