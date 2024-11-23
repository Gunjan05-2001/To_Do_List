import tkinter as tk
from tkinter import messagebox
import json

# Constants for styling
BG_COLOR = "#fef9e7"  # Soft cream
BUTTON_NORMAL = "#3498db"  # Bright blue
BUTTON_HOVER = "#2980b9"  # Darker blue on hover
BUTTON_FG = "#ffffff"  # White text
FONT_MAIN = ("Verdana", 12)
FONT_TITLE = ("Verdana", 18, "bold")
LISTBOX_BG = "#ffffff"
LISTBOX_FG = "#34495e"  # Dark gray text

# Functions
def add_task():
    """Adds a new task to the listbox."""
    task = task_entry.get().strip()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

def delete_task():
    """Deletes the selected task."""
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete!")

def clear_tasks():
    """Clears all tasks."""
    if messagebox.askyesno("Confirm", "Do you want to clear all tasks?"):
        task_listbox.delete(0, tk.END)

def save_tasks():
    """Saves tasks to a JSON file."""
    tasks = task_listbox.get(0, tk.END)
    with open("tasks.json", "w") as file:
        json.dump(list(tasks), file)
    messagebox.showinfo("Success", "Tasks saved successfully!")

def load_tasks():
    """Loads tasks from a JSON file."""
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        task_listbox.delete(0, tk.END)
        for task in tasks:
            task_listbox.insert(tk.END, task)
    except FileNotFoundError:
        messagebox.showwarning("File Error", "No saved tasks found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to load tasks.")

def edit_task():
    """Edits the selected task."""
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        new_task = task_entry.get().strip()
        if new_task:
            task_listbox.delete(selected_task_index)
            task_listbox.insert(selected_task_index, new_task)
            task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to edit!")

def mark_task_complete():
    """Marks the selected task as complete."""
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = task_listbox.get(selected_task_index)
        task_listbox.delete(selected_task_index)
        task_listbox.insert(tk.END, f"{task} ✓")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as complete!")

# Button hover effects
def on_hover(event):
    event.widget.config(bg=BUTTON_HOVER)

def on_leave(event):
    event.widget.config(bg=BUTTON_NORMAL)

# Main Application
root = tk.Tk()
root.title("To-Do List")
root.geometry("500x550")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Title Label
title_label = tk.Label(root, text="Modern To-Do List", font=FONT_TITLE, bg=BG_COLOR, fg="#2c3e50")
title_label.pack(pady=20)

# Input Frame
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=35, font=FONT_MAIN)
task_entry.grid(row=0, column=0, padx=5)

add_button = tk.Button(input_frame, text="Add Task", font=FONT_MAIN, bg=BUTTON_NORMAL, fg=BUTTON_FG, command=add_task)
add_button.grid(row=0, column=1, padx=5)

# Add hover effect to the button
add_button.bind("<Enter>", on_hover)
add_button.bind("<Leave>", on_leave)

# Listbox Frame
listbox_frame = tk.Frame(root, bg=BG_COLOR)
listbox_frame.pack(pady=10)

task_listbox = tk.Listbox(
    listbox_frame, width=55, height=15, font=FONT_MAIN, selectmode=tk.SINGLE, bg=LISTBOX_BG, fg=LISTBOX_FG
)
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=task_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox.config(yscrollcommand=scrollbar.set)

# Buttons Frame
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=15)

buttons = [
    ("Delete", delete_task),
    ("Edit", edit_task),
    ("Mark Complete", mark_task_complete),
    ("Clear All", clear_tasks),
    ("Save", save_tasks),
    ("Load", load_tasks),
]

for i, (text, command) in enumerate(buttons):
    button = tk.Button(button_frame, text=text, font=FONT_MAIN, bg=BUTTON_NORMAL, fg=BUTTON_FG, command=command)
    button.grid(row=i // 3, column=i % 3, padx=10, pady=5, ipadx=10)

    # Add hover effects
    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

# Run the Application
root.mainloop()