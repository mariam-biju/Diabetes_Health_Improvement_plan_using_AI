# 🩺 Diabetes Health Plan - A* Search Health Improvement

A **Tkinter-based application** that uses the **A* search algorithm** to recommend the best health improvement path for individuals aiming to lower their blood sugar levels. The system takes into account key factors such as BMI, activity score, and blood sugar level, providing personalized suggestions and visualizing progress over time.

---

## 📊 Key Features

- ✅ Uses **A* search** to find the optimal health improvement path.
- ✅ Takes **BMI**, **activity score**, and **blood sugar levels** as inputs.
- ✅ Suggests gradual **BMI** and **activity score** changes to lower blood sugar.
- ✅ Visualizes health progress with **Matplotlib** graphs (BMI, activity score, and blood sugar over time).
- ✅ User-friendly **Tkinter GUI** to enter health data and view results.

---

## 🧠 How It Works

1. **User Input**: Enter BMI, age, activity score, and blood sugar level.
2. **A* Search**: The system searches for the best health improvement path to reduce blood sugar levels.
3. **Health Suggestions**: Gradual changes in BMI and activity score are suggested to improve health.
4. **Visualization**: The program plots the progress (BMI, activity score, blood sugar) over time.

Example:
```
Input: BMI = 25, Age = 40, Activity Score = 50, Blood Sugar = 180
Output: Path found with suggestions to reduce blood sugar to the target level (120).
```

---

## 🛠 Tech Stack

- 🐍 Python 3.x  
- 🌐 Tkinter (GUI)  
- 📊 Matplotlib (Visualization)  
- 🧠 A* Search Algorithm  
- 💾 heapq (Priority Queue for A*)

---

## 📁 Project Structure

```
diabetes-health-plan/
├── health_plan.py        # Main application with logic
├── templates/             # Directory for UI components
│   └── index.html        # HTML file for front-end (if needed)
├── assets/                # Directory for any additional assets
```

---

## 📦 Dependencies

Install with:

```
pip install matplotlib
```

---

## ▶️ How to Run

1. Clone the repository or download the code.
2. Place the script in the working directory.
3. Run the app:

```
python health_plan.py
```

4. Open the app in your system's Tkinter window and input your health data.

---

## 🗃️ Example Inputs & Outputs

- **Input**:  
  BMI = 30, Age = 45, Activity Score = 60, Blood Sugar = 200  
- **Output**:  
  Path found to reduce blood sugar level with suggested BMI and activity score changes.

---

## ⚠️ Notes

- **Sensitivity Constants** (`alpha`, `beta`): Control how much BMI and activity changes affect blood sugar levels.
- **Target Blood Sugar**: The goal is to reduce the blood sugar level to **120** or lower.
- **Visualization**: Plots include BMI, activity score, and blood sugar level over time.

---
