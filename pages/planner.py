import datetime 
import tkinter as tk
import db
from pages.calendarPage import CalendarPage
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
        start_button = tk.Button(self, text="Generate Weekly Plan", command=self.generate_weekly_planner)
        start_button.pack()

    # function to generate planner
    def generate_weekly_planner(self):

        try:

            tasks = self.get_weekly_tasks()

            # define time slots from 10am to 8pm
            timeslot = [
                "10:00 - 11:00",
                "11:00 - 12:00",
                "12:00 - 13:00",
                "13:00 - 14:00",
                "14:00 - 15:00",
                "15:00 - 16:00",
                "16:00 - 17:00",
                "17:00 - 18:00",
                "18:00 - 19:00",
                "19:00 - 20:00",
            ]

            # assign tasks to time slots 
            assigned_tasks = self.assign_to_time_slot(tasks, timeslot)
            
            # schedule tasks and create calendar event
            self.schedule_events(assigned_tasks)

        except Exception as e:
            print(f"An error has occured: ", e)

    # function to get tasks
    def get_weekly_tasks(self):
        weekly_tasks = db.get_task()
        print(weekly_tasks)
        return weekly_tasks
        
    # function to assign tasks to time slots based on priority level and nearest available time slot
    def assign_to_time_slot(self, tasks, timeslot):
        assigned_tasks = {}
        task_list = []

        # Create a list of tasks with their priority levels
        for task_title, task_data in tasks.items():
            if isinstance(task_data, dict):
                priority_level = task_data.get('priority_level', 0)
                task_list.append((task_title, priority_level))

        # Sort tasks by priority level if available, or use a default priority of 0
        sorted_tasks = sorted(task_list, key=lambda x: x[1], reverse=True)

        for task_title, priority_level in sorted_tasks:
            # Find the nearest available time slot
            nearest_slot = self.find_nearest_available_slot(timeslot, assigned_tasks)
            if nearest_slot:
                assigned_tasks[nearest_slot] = {
                    "task_text": task_title,
                    "priority_level": priority_level
                }

        return assigned_tasks

    # Function to get the next timeslot (e.g., move from "10:00 - 11:00" to "11:00 - 12:00")
    def get_next_timeslot(self, current_timeslot):
        # Split the current timeslot into start and end times
        start_time, end_time = current_timeslot.split(" - ")

        # Increment the start and end times by one hour
        start_time_parts = start_time.split(":")
        end_time_parts = end_time.split(":")
        start_hour = int(start_time_parts[0])
        end_hour = int(end_time_parts[0])

        # Increment the hours and ensure the end time does not exceed 9:00 PM (21:00)
        start_hour += 1
        end_hour += 1
        if end_hour > 21:
            end_hour = 21

        # Format the updated times
        updated_start_time = f"{start_hour:02d}:00"
        updated_end_time = f"{end_hour:02d}:00"

        # Combine the updated times into a new timeslot
        next_timeslot = f"{updated_start_time} - {updated_end_time}"

        return next_timeslot

    # function to split timeslot into start + end times
    def parse_timeslot(self, timeslot):
        start_time, end_time = timeslot.split("-")
        return start_time, end_time

    # function to schedule events
    def schedule_events(self, assigned_tasks):

        calendar_page = CalendarPage()
        for task_title, timeslot in assigned_tasks.items():

            #define details
            event_title = task_title["task_text"]
            event_description = "grind time baby"

            #parse the ime slot
            event_start_time, event_end_time = self.parse_timeslot(timeslot)

            #event_end_time = self.calculate_end_time(event_start_time)

            calendar_page.add_event(event_title, event_description, event_start_time, event_end_time)

            print("Added event", event_title, "to", event_start_time)

    # function to calculate an hour after event start time
    def calculate_end_time(self, event_start_time):
        # parse start time to get hour and minutes
        start_hour, start_minute = map(int, event_start_time.split(':'))

        # calculate end hour and minute
        end_hour = start_hour + 1
        end_minute = start_minute

        # ensure it does not surpass 9pm
        if end_hour > 21: 
            end_hour = 21
            end_minute = 0

        # format end time
        end_time = f"{end_hour:02d}:{end_minute:02d}"

        return end_time
