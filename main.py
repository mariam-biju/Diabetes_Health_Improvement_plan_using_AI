import tkinter as tk
import heapq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants for sensitivity
alpha = 8.5  # Sensitivity of BMI change
beta = 3   # Sensitivity of Activity score change

# Target blood sugar level
TARGET_BLOOD_SUGAR = 120

# Define the Node class
class HealthNode:
    def __init__(self, bmi, age, activity_score, blood_sugar, suggestions=None, parent=None):
        self.bmi = bmi
        self.age = age
        self.activity_score = activity_score
        self.blood_sugar = blood_sugar  # represents the current diabetes risk level
        self.suggestions = suggestions or []  # suggestions for improvement
        self.parent = parent

    def __lt__(self, other):
        return self.blood_sugar < other.blood_sugar
    
    def __repr__(self):
        return f"(BMI: {self.bmi}, Activity: {self.activity_score}, Blood Sugar: {self.blood_sugar})"


# Heuristic function: estimates how far the current state is from the goal
def heuristic(state):
    # Heuristic is the absolute difference from the target blood sugar level
    return abs(state.blood_sugar - TARGET_BLOOD_SUGAR)

# Cost function: Calculate cost based on BMI and Activity changes
def cost_function(current, child):
    # Cost is the total effort in changing BMI and Activity score
    bmi_change = abs(current.bmi - child.bmi)
    activity_change = abs(current.activity_score - child.activity_score)
    return bmi_change + activity_change

# Function to calculate the new blood sugar level after a change in BMI and Activity
def update_blood_sugar(bmi_change, activity_change, current_blood_sugar):
    # Apply the change to the blood sugar level based on the formula
    reduction = alpha * bmi_change + beta * activity_change
    new_blood_sugar = max(80, current_blood_sugar - reduction)  # Ensure blood sugar doesn't go below 80
    return new_blood_sugar


# A* search algorithm to find the best health improvement path
def a_star_search(start_state):
    # Priority queue for the frontier
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state), start_state))
    
    # Explored set to avoid revisiting states
    explored = set()

    while frontier:
        # Get the node with the lowest estimated cost
        current_f_cost, current_state = heapq.heappop(frontier)

        # If we reach the goal, return the solution path
        if current_state.blood_sugar <= TARGET_BLOOD_SUGAR:
            return current_state

        # Mark current state as explored
        explored.add((current_state.bmi, current_state.activity_score, current_state.blood_sugar))
        print("---------------",current_state.blood_sugar,current_state.bmi, current_state.activity_score,"-----")
        # Generate child nodes (new BMI or Activity change)
        for bmi_change, activity_change in [(0.8, 0), (0, 5)]:  # Small gradual changes
            new_bmi = current_state.bmi - bmi_change
            new_activity_score = current_state.activity_score + activity_change
            new_blood_sugar = update_blood_sugar(bmi_change, activity_change, current_state.blood_sugar)

            new_state = HealthNode(new_bmi, current_state.age, new_activity_score, new_blood_sugar, parent=current_state)

            # Check if the new state has been explored
            if (new_state.bmi, new_state.activity_score, new_state.blood_sugar) not in explored:
                # Calculate total cost and push the new state to the frontier
                g_cost = cost_function(current_state, new_state)
                f_cost = g_cost + heuristic(new_state)
                heapq.heappush(frontier, (f_cost, new_state))

    return None  # No solution found

# Build the user interface (UI) using tkinter
def submit_data():
    bmi = float(bmi_entry.get())
    age = int(age_entry.get())
    activity_score = int(activity_entry.get())
    blood_sugar = float(diabetes_entry.get())  # Get user-provided diabetes level

    # Example suggestions for health improvement
    suggestions = [
        {'bmi_change': 2, 'activity_change': 5, 'next_suggestions': []},
        {'bmi_change': 0.5, 'activity_change': 6, 'next_suggestions': []},
    ]

    # Define the start node with input data
    start_node = HealthNode(bmi=bmi, age=age, activity_score=activity_score, blood_sugar=blood_sugar, suggestions=suggestions)
    #goal_level = 50  # The goal is to reduce the diabetes level to 50 or below
    
    result_node = a_star_search(start_node)

    if result_node:
        result_label.config(text="Health improvement path found!")
        display_path(result_node)
        plot_graph(result_node)
    else:
        result_label.config(text="No valid path to improve health.")

# Function to display the health improvement path
def display_path(node):
    path = []
    while node:
        path.append(f"BMI: {node.bmi}, Age: {node.age}, Activity: {node.activity_score}, Diabetes Level: {node.blood_sugar}")
        node = node.parent
    path.reverse()
    path_label.config(text="\n".join(path))

# Function to extract the path data for plotting
def extract_path_data(node):
    bmi_values = []
    activity_values = []
    blood_sugar_values = []
    
    # Traverse the path from the result node to the start node using the parent references
    while node:
        bmi_values.append(node.bmi)
        activity_values.append(node.activity_score)
        blood_sugar_values.append(node.blood_sugar)
        node = node.parent
    
    # Reverse the lists so the path starts from the initial state
    bmi_values.reverse()
    activity_values.reverse()
    blood_sugar_values.reverse()
    
    return bmi_values, activity_values, blood_sugar_values
# Function to plot the graph with specified ranges


# Function to plot the graph with specified ranges
def plot_graph(node):
    bmi_values, activity_values, blood_sugar_values = extract_path_data(node)

    # Assume we want to represent the data over 6 months
    time_points = list(range(1, len(bmi_values) + 1))  # Generating time points (e.g., 1, 2, ..., 6 if 6 points)

    fig, ax = plt.subplots(3, 1, figsize=(6, 8))

    # Plot BMI values
    ax[0].plot(time_points, bmi_values, marker='o', color='blue', label='BMI')
    ax[0].set_title('BMI x Time')
    ax[0].set_ylabel('BMI')
    ax[0].set_ylim(14, 30)  # Setting y-axis range for BMI
    ax[0].set_xticks(time_points)
    ax[0].set_xticklabels([f' {i}' for i in time_points])
    ax[0].legend()

    # Plot Activity Score values
    ax[1].plot(time_points, activity_values, marker='o', color='green', label='Activity Score')
    ax[1].set_title('Activity Score x Time')
    ax[1].set_ylabel('Activity Score')
    ax[1].set_ylim(0, 100)  # Setting y-axis range for Activity Score
    ax[1].set_xticks(time_points)
    ax[1].set_xticklabels([f'{i}' for i in time_points])
    ax[1].legend()

    # Plot Blood Sugar values
    ax[2].plot(time_points, blood_sugar_values, marker='o', color='red', label='Blood Sugar Level')
    ax[2].set_title('Blood Sugar Level x Time ')
    ax[2].set_ylabel('Blood Sugar Level')
    ax[2].set_ylim(100, 400)  # Setting y-axis range for Blood Sugar Level
    ax[2].set_xticks(time_points)
    ax[2].set_xticklabels([f'{i}' for i in time_points])
    ax[2].legend()

    # Set the main title for the entire plot
    fig.suptitle("Growth Plan", fontsize=16)

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit title

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=7)  # Place graph in the right column

# Creating the UI
root = tk.Tk()
root.title("Diabetes Health Plan")

# Left column: User input fields
tk.Label(root, text="BMI:").grid(row=0, column=0)
bmi_entry = tk.Entry(root)
bmi_entry.grid(row=0, column=1)

tk.Label(root, text="Age:").grid(row=1, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)

tk.Label(root, text="Activity Score (0-100):").grid(row=2, column=0)
activity_entry = tk.Entry(root)
activity_entry.grid(row=2, column=1)

tk.Label(root, text="Current Diabetes Level:").grid(row=3, column=0)  # New input field for diabetes level
diabetes_entry = tk.Entry(root)
diabetes_entry.grid(row=3, column=1)

submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=4, column=1)

result_label = tk.Label(root, text="")
result_label.grid(row=5, column=1)

path_label = tk.Label(root, text="", justify="left")
path_label.grid(row=6, column=1)

# Run the UI main loop
root.mainloop()
