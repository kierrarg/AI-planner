import tkinter as tk
from tkinter import ttk
import db

# Define the TaskListPage class with its content
class TaskListPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#ADD8E6")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="This is the Task List Page")
        label.pack(fill="both", expand=True)

        #frame for task input
        input_frame = tk.Frame(self, bg="#ADD8E6")
        input_frame.pack(side="left", padx=10, pady=10, anchor="w")

        task_label = tk.Label(input_frame, text="Task:", font=("Arial", 10))
        task_label.pack(anchor="w")

        task_entry= tk.Entry(input_frame, width=30)
        task_entry.pack(fill="x", padx=5, pady=5)

        priority_label = tk.Label(input_frame, text="Priority (1-5):", font=("Arial", 10))
        priority_label.pack(anchor="w")

        priority_entry = tk.Entry(input_frame, width=5)
        priority_entry.pack(fill="x", padx=5, pady=5)

        # Create a Treeview widget to display tasks
        task_treeview = ttk.Treeview(self, columns=("Task", "Priority"), selectmode=tk.EXTENDED)
        task_treeview.heading("#1", text="Task")
        task_treeview.heading('#2', text="Priority")

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=task_treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        task_treeview.config(yscrollcommand=scrollbar.set)

        task_treeview.pack(fill="both", expand=True)

        # Button for adding task and marking as complete
        add_button = tk.Button(self, text="Add Task", command=lambda: self.add_task(task_entry, priority_entry, task_treeview))
        add_button.pack(side="left")

        complete_button = tk.Button(self, text="Mark Completed", command=lambda: self.mark_complete(task_treeview))
        complete_button.pack(side="left")

        
        delete_button = tk.Button(self, text="Delete", command=lambda: self.delete_task(task_treeview))
        delete_button.pack(side="left")

        # Fetch and display from db
        self.fetch_display(task_treeview)

    # Fetching and displaying tasks from db
    def fetch_display(self, task_treeview):
        # Fetch tasks
        tasks = db.get_task()

        # Check if tasks is empty
        if not tasks:
            return  # Don't proceed if tasks are empty

        # Clear Treeview
        task_treeview.delete(*task_treeview.get_children())

        # Display tasks in Treeview with the task text aligned to the left
        for task_text in tasks:
            completed = db.get_completion(tasks[task_text])  # Get task completion status using task_text's ID
            priority_level = db.get_priority_level(tasks[task_text])

            if completed:
                # Apply a custom style for completed tasks
                task_text = " [Completed] " + task_text  # Add [Completed] prefix
                task_treeview.insert("", "end", values=(task_text, priority_level), tags=("completed",))
            else:
                task_treeview.insert("", "end", values=(task_text, priority_level), tags=("incomplete"))

        # Configure the custom style for completed tasks
        task_treeview.tag_configure("completed", font=("TkDefaultFont", 12, "overstrike"))
        task_treeview.tag_configure("incomplete", font=("TkDefaultFont", 12))

    # Add task to Treeview
    def add_task(self, task_entry, priority_entry, task_treeview):
        # Get text from widget
        new_task_text = task_entry.get()
        priority_level = priority_entry.get()

        # ensure priority level is an integer
        try:
            priority_level = int(priority_level)
            priority_level = max(1, min(priority_level, 5)) #limiting allowed priority level
        except ValueError:
            priority_level = 1 #default to 1 if not valid int

        # Insert task into db
        db.insert(new_task_text, priority_level)

        # Clear widget
        task_entry.delete(0, tk.END)
        priority_entry.delete(0, tk.END)

        # Fetch and display in Treeview
        self.fetch_display(task_treeview)

    # Mark tasks as complete
    def mark_complete(self, task_treeview):
        # Get selected tasks
        selected_task_indices = task_treeview.selection()

        # Mark tasks as completed in the database
        for index in selected_task_indices:
            task_text = task_treeview.item(index, "values")[0]  # get task text from tree view
            task_id = db.get_task().get(task_text) # get task id using task text
            if task_id is not None:
                completed = db.get_completion(task_id)
                if completed:
                    # remove tag
                    task_treeview.item(index, tags=())
                    db.update(task_text, 0)
                else:
                    # apply tag
                    task_treeview.item(index, tags=("completed"))
                    db.update(task_text, 1) # mark as complete in db

        # Fetch and display updated tasks
        self.fetch_display(task_treeview)

    # Delete tasks
    def delete_task(self, task_treeview):
        # Get selected tasks
        selected_tasks_indices = task_treeview.selection()
        
        # Delete selected task from db
        for index in selected_tasks_indices:
            task_text = task_treeview.item(index, "values")[0]  # Get the task text from the Treeview
            db.delete(task_text)  # Delete the task directly by passing task_text

        # Refresh the Treeview
        self.fetch_display(task_treeview)