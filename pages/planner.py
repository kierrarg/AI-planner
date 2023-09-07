import datetime 
import tkinter as tk
import db
#from googleapiclient import build 
#from google.oauth2.credentials import Credentials
#from google.auth.transport.requests import Request 


class PlannerPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#ADD8E6")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="This is the planner page")
        label.pack(fill="both", expand=True)

    # function to generate planner
    def generate_weekly_planner():
        pass

        # tasks = get_weekly_tasks()

        # define time slots from 10am to 8pm

        # assign tasks to time slots 
        
        # schedule tasks and create calendar event

        # handle overlaps and conflicts

        # remove completed tasks and google calendar event

        # create study and assignment blocks based on due dates and keywords 

    # function to get tasks
    def get_weekly_tasks():
        pass
        # return tasks as a list
