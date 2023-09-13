import datetime 
import tkinter as tk
import db
from pages.calendarPage import CalendarPage
import traceback
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
        print("calling create widgets")
        label = tk.Label(self, text="This is the planner page")
        label.pack(fill="both", expand=True)
        start_button = tk.Button(self, text="Generate Weekly Plan", command=self.generate_weekly_planner)
        start_button.pack()

    # function to generate planner
    def generate_weekly_planner(self):
        print("calling generate weekly planner")

        try:
            tasks = self.get_weekly_tasks()

            # define time slots from 10am to 8pm
            timeslots = [
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

            assigned_tasks = {}  # Initialize assigned tasks dictionary

            # assign tasks to time slots
            for timeslot in timeslots:
                assigned_tasks = self.assign_to_time_slot(tasks, timeslot, assigned_tasks, timeslots, event_date=datetime.date.today())
                print(f"Assigned tasks for timeslot {timeslot}: {assigned_tasks}")

                # Check if all tasks have been assigned
                if len(assigned_tasks) == len(tasks):
                    break  # All tasks are assigned, break the loop

             # Call the schedule_events function
            self.schedule_events(assigned_tasks)

        except Exception as e:
            print(f"An error has occurred: ", e)

    # function to get tasks
    def get_weekly_tasks(self):
        print("Calling get weekly tasks")
        weekly_tasks = db.get_task()
        print(weekly_tasks)

        # dictionary to store tasks
        tasks_with_priority = {}

        for task_name, task_id in weekly_tasks.items():
            # fetch priority level for each task
            priority_level = db.get_priority_level(task_id)
            tasks_with_priority[task_name] = priority_level
            print(tasks_with_priority)

        return tasks_with_priority
        
    # function to assign tasks to time slots based on priority level and nearest available time slot
    def assign_to_time_slot(self, tasks, timeslot, assigned_tasks, timeslots, event_date):
        print("Calling assign to timeslot")
        task_list = []
        calendar_page = CalendarPage()

        print("Timeslot: ", timeslot)

        # Create a list of tasks with their priority levels
        for task_title, priority_level in tasks.items():
            print("Entering 1st for loop")
            task_list.append((task_title, priority_level))
            print(task_list)

        # Sort tasks by priority level if available, or use a default priority of 0
        sorted_tasks = sorted(task_list, key=lambda x: x[1], reverse=True)

        print("Sorted tasks: ", sorted_tasks)

        # Initialize available time slots as a copy of the original time slots
        available_time_slots = timeslots.copy()

        for task_title, priority_level in sorted_tasks:
            # Find the nearest available time slot based on priority
            nearest_slot = None

            for slot in available_time_slots:
                print("Inside 2nd for loop")
                start_time, _ = self.parse_timeslot(slot)
                print(start_time)
                start_hour = int(start_time.split(":")[0])
                print("Start hour: ", start_hour)

                # Check if the priority matches or is higher than the task's priority
                if priority_level >= tasks[task_title]:
                    # Check if the time slot is not already assigned
                    if slot not in assigned_tasks:
                        nearest_slot = slot
                        break  # Assign the task to the first available slot

            print("Current Timeslot: ", timeslot)
            print("Assigned tasks before adding", assigned_tasks)
            print("Nearest slot: ", nearest_slot)
            if nearest_slot:
                # Parse the nearest slot to get start and end times
                nearest_start_time, nearest_end_time = self.parse_timeslot(nearest_slot)
                # Combine the event_date with start and end times
                event_start_datetime = datetime.datetime.combine(event_date, datetime.datetime.strptime(nearest_start_time, "%H:%M").time())
                event_end_datetime = datetime.datetime.combine(event_date, datetime.datetime.strptime(nearest_end_time, "%H:%M").time())
                
                # Check if the nearest slot is available
                if not calendar_page.is_timeslot_assigned(event_start_datetime, event_end_datetime):
                    assigned_tasks[nearest_slot] = {
                        "task_text": task_title,
                        "priority_level": priority_level,
                        "event_date": event_date
                    }
                    # Remove the assigned slot from available slots
                    available_time_slots.remove(nearest_slot)
                    print("Assigned tasks after adding", assigned_tasks)

            next_available_slot = self.get_next_timeslot(timeslot, available_time_slots)

        return assigned_tasks
    

    # function to find nearest time slot
    def find_nearest_available_slot(self, timeslot, assigned_tasks):
        # start time of provided slot
        print("calling find nearest available timeslot")
        print(timeslot)
        current_start_time, _ = self.parse_timeslot(timeslot)
        print("Find nearest timeslot timeslot: ", timeslot)

        # convert to integer for comparison
        current_start_hour = int(current_start_time.split(":")[0])
        print("Current start hour: ", current_start_hour)

        # initialize variables to keep track of closest slot 
        closest_slot = None
        min_time_difference = float('inf') # initialize w/ positive infinity

        if not assigned_tasks:
            return timeslot

        # iterate over time slots
        for slot in assigned_tasks.keys():
            print("inside for loop")
            start_time, _ = self.parse_timeslot(slot)
            print(start_time)
            start_hour = int(start_time.split(":")[0])
            print("Start hour: ", start_hour)
           
            # calculate time difference 
            time_difference = start_hour - current_start_hour
            print("Time difference: ", time_difference)

            #check which slot is closer
            if time_difference >= 0 and time_difference < min_time_difference:
                closest_slot = slot
                min_time_difference = time_difference
         
        return closest_slot
    

    # Function to get the next timeslot (e.g., move from "10:00 - 11:00" to "11:00 - 12:00")
    def get_next_timeslot(self, current_timeslot, timeslots):
        print("Calling get next timeslot")
        # find the index of the current timeslot
        try:
            current_index = timeslots.index(current_timeslot)
        except ValueError:
            return None # timeslot is not in list
        
        # if next timeslot is available
        if current_index < len(timeslots) - 1:
            return timeslots[current_index + 1]
        else:
            return None # next timeslot not available

    # function to split timeslot into start + end times
    def parse_timeslot(self, timeslot):
        print("Calling parse timeslot")
        start_time, end_time = timeslot.split("-")
        # add strip() to remove white spaces
        return start_time.strip(), end_time.strip()

    # function to schedule events
    def schedule_events(self, assigned_tasks):
        print("Calling schedule events")
        calendar_page = CalendarPage()
        print("Entering for loop")
        print(assigned_tasks)
        
        for timeslot, task_info in assigned_tasks.items():
            print("Inside for loop")
            print("Timeslot: ", timeslot)
            print("Assigned tasks: ", assigned_tasks)

            try:
                # Define details
                event_title = task_info["task_text"]
                event_description = "grind time baby"
                print("Inside try block - Adding event: ", event_title)

                # Parse the time slot and remove leading/trailing whitespace
                event_start_time_str, event_end_time_str = self.parse_timeslot(timeslot)

                # Convert start and end time strings to datetime.time objects
                event_start_time = datetime.datetime.strptime(event_start_time_str, "%H:%M").time()
                event_end_time = datetime.datetime.strptime(event_end_time_str, "%H:%M").time()

                # get event date associated with timeslot
                event_date = task_info.get("event_date")

                if event_date is None:
                    print(f"Event date missing for timeslot {timeslot}")
                    continue

                # Create datetime objects for time with the current date
                event_start_datetime = datetime.datetime.combine(event_date, event_start_time)
                event_end_datetime = datetime.datetime.combine(event_date, event_end_time)

                # specify timezone
                event_start_datetime = event_start_datetime.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-6)))
                event_end_datetime = event_end_datetime.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-6)))

                # Format as string
                event_start_time_str = event_start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                event_end_time_str = event_end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

                print("Adding event: ", event_title)
                print("Start Time: ", event_start_time_str)
                print("End Time: ", event_end_time_str)

                if calendar_page.is_timeslot_assigned(event_start_datetime, event_end_datetime):
                    print(f"Time slot {timeslot} is already assigned, skipping to next time slot {timeslot}")
                    continue

                calendar_page.add_event(event_title, event_description, event_start_datetime, event_end_datetime)

                print("Added event", event_title, "to", event_start_time_str)
            
            except Exception as e:
                print(f"An error has occurred: {e}")
                traceback.print_exc()


    # function to calculate an hour after event start time
    def calculate_end_time(self, event_start_time):
        # parse start time to get hour and minutes
        print("Calling calculate end time")
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

