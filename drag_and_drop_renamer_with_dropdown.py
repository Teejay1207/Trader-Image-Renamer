import tkinter as tk
from tkinter import messagebox, ttk
import os
import json
import sys

# Function to process the file
def process_file(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext in ['.jpg', '.png']:
        selected_name = name_var.get()
        new_name = name_list.get(selected_name)
        if new_name:
            new_path = os.path.join(os.path.dirname(file_path), new_name + file_ext)
            os.rename(file_path, new_path)
            messagebox.showinfo("Success", f"File renamed to {new_name}{file_ext}")
            root.quit()  # Close the application after renaming
        else:
            messagebox.showerror("Error", "No name selected")
    else:
        messagebox.showerror("Error", "Please use a JPG or PNG file")

# Function to load the JSON file and update the dropdown menu
def refresh_names():
    global name_list
    try:
        with open('namelist.json', 'r') as file:
            name_list = json.load(file)
        name_dropdown['values'] = list(name_list.keys())
        name_dropdown.set("Select a name")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load names: {e}")

# Function to initialize the GUI
def initialize_gui(file_path=None):
    global name_var, name_dropdown, root

    # Create the main application window
    root = tk.Tk()
    root.title("Trader Image Renamer")
    root.geometry("400x200")

    # Create a label to instruct the user
    label_text = "Please select a trader name"
    if file_path:
        label_text = f"File to process: {file_path}"
    label = tk.Label(root, text=label_text, pady=10)
    label.pack()

    # Create a dropdown menu for name selection
    name_var = tk.StringVar()
    name_dropdown = ttk.Combobox(root, textvariable=name_var, state='readonly')
    name_dropdown.pack(pady=10)

    # Create a refresh button to reload the JSON file
    refresh_button = tk.Button(root, text="Refresh Names", command=refresh_names)
    refresh_button.pack(pady=10)

    # Create a button to process the file if it's already provided
    if file_path:
        process_button = tk.Button(root, text="Rename File", command=lambda: process_file(file_path))
        process_button.pack(pady=10)

    # Initial load of names
    refresh_names()

    # Run the main loop
    root.mainloop()

# Check if a file path was passed as an argument (for drag and drop on the exe)
if len(sys.argv) > 1:
    file_path_to_process = sys.argv[1]
    initialize_gui(file_path_to_process)
else:
    messagebox.showerror("Error", "No file provided. Please drag and drop a JPG or PNG file onto the executable.")
