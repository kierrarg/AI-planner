import tkinter as tk
from tkinter import ttk
import db
from pages.taskPage import TaskListPage
from pages.calendarPage import CalendarPage
from pages.planner import PlannerPage

#function to initialize the database
def initialize_db():
    db.create_db()

# Creating custom GUI by extending tk.Frame
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.current_page = None  # Initialize the current page
        self.pack(fill="both", expand=True)
        self.configure(bg="#ADD8E6")
        self.create_widgets()
        self.show_home()  # Show main buttons on initialization

    def create_widgets(self):
        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="bottom", fill="x")

        # Create and pack the main page buttons
        self.navigation_frame = tk.Frame(self)
        self.navigation_frame.pack(side="top", fill="x")

        self.calendar_button = tk.Button(self.navigation_frame, text="Calendar", command=self.show_calendar)
        self.calendar_button.pack(side="left")

        self.tasks_button = tk.Button(self.navigation_frame, text="Tasks", command=self.show_tasks)
        self.tasks_button.pack(side="left")

        self.planner_button = tk.Button(self.navigation_frame, text="Planner", command=self.show_planner)
        self.planner_button.pack(side="left")

        self.home_button = tk.Button(self.navigation_frame, text="Home", command=self.show_home)
        self.home_button.pack(side="left")

    def remove_widgets(self):
        # Remove all widgets from the current page
        if self.current_page is not None:
            self.current_page.destroy()
            self.current_page = None

    def show_home(self):
        # Remove widgets from the current page
        self.remove_widgets()

        # Re-display the main page widgets
        self.show_main_buttons()  # Show main buttons on the home page

    # displaying top navigation bar
    def show_main_buttons(self):
        self.calendar_button.pack(side="left")
        self.tasks_button.pack(side="left")
        self.planner_button.pack(side="left")
        self.home_button.pack(side="left")
        self.quit_button.pack(side="bottom", fill="x")

    def show_calendar(self):
        # Remove widgets from the current page
        self.remove_widgets()

        # Create and display the Calendar page
        self.current_page = CalendarPage(self)
        self.current_page.pack(fill="both", expand=True)

    def show_tasks(self):
        # Remove widgets from the current page
        self.remove_widgets()

        # Create and display the Tasks page
        self.current_page = TaskListPage(self)
        self.current_page.pack(fill="both", expand=True)

    def show_planner(self):
        # Remove widgets from the current page
        self.remove_widgets()

        # Create and display the Planner page
        self.current_page = PlannerPage(self)
        self.current_page.pack(fill="both", expand=True)


if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    root.geometry("800x600")

    app = Application(master=root)

    app.mainloop()