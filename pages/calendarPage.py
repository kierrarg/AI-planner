import tkinter as tk
from tkinter import ttk
import db

# Define the CalendarPage class with its content
class CalendarPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#ADD8E6")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="This is the Calendar Page")
        label.pack(fill="both", expand=True)

        #frame to contain grid buttons
        calendar_frame = tk.Frame(self)
        calendar_frame.pack()

        # list of weekday labels
        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        #weekday labels at top
        for col, weekday in enumerate(weekdays):
            weekday_label = tk.Label(calendar_frame, text=weekday)
            weekday_label.grid(row=0, column=col)

        #create a grid of buttons for each day of the month
        for row in range(1, 6): #rows for calendar grid
            for col in range(7): #columns for days of week
                day_button = tk.Button(calendar_frame, text="", width=3, height=1)
                day_button.grid(row=row, column=col, padx=5, pady=5)
        
        #creating arrow frames
        arrow_frame = tk.Frame(self)
        arrow_frame.pack()

        #arrows for month navigation
        left_arrow = tk.Button(arrow_frame, text="<")
        left_arrow.grid(row=0, column=0)
        right_arrow = tk.Button(arrow_frame, text=">")
        right_arrow.grid(row=0, column=6)

    def prev_month(self):
        #change to previous month
        self.current_month = (self.current_month - 1) % 12
        self.update_month_label()

    def next_month(self):
        # change to next month
        self.current_month = (self.current_month + 1) % 12
        self.update_month_label()
    
    def update_month_label(self):
        #update month label
        months = ["January", "February", "March", "April", "May"]

#Page to add events
class AddEventPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="ADD8E6")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Add Event")
        label.pack(fill="both", expand=True)

        #entry fields for details
        event_name_label = tk.Label(self, text="Event Name:")
        event_name_label.pack()
        event_name_entry = tk.Entry(self)
        event_name_entry.pack()

        event_date_label = tk.Label(self, text="Event Date:")
        event_date_label.pack()
        event_date_entry = tk.Entry(self)
        event_date_entry.pack()

        event_time_label = tk.Label(self, 
        text="Event Time:")
        event_time_label.pack()
        event_time_entry = tk.Entry(self)
        event_time_entry.pack()

        #add_event_button = tk.Button(self, text="Add Event", command=lambda: self.#add_event(event_name_entry, event_date_entry, event_time_entry))
        #add_event_button.pack()

    #def add_event(self, even_name_entry, event_date_entry, event_time_entry)
        
       # event_name = even_name_entry.get()
       # event_date = event_date_entry.get()
       # event_time = event_time_entry.get()
