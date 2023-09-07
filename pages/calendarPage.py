import tkinter as tk
from tkinter import simpledialog as tk_simpledialog
import calendar
import datetime
import logging
from pages.goog import create_calendar_service, create_event, delete_custom_event_by_title
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Define the scopes you need for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Specify fixed redirect URI
REDIRECT_URI = 'http://localhost:8090/oauth2callback'

# Create a Google Calendar service
calendar_service = create_calendar_service('credentials.json', 'token files', 'calendar', 'v3', SCOPES, prefix='')

class CalendarPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#ADD8E6")
        self.current_month = 9  # Set the initial month (e.g., August)
        self.current_year = 2023  # Set the initial year
        self.single_event_clicked_day = 1 # Initialize clicked day
        self.single_event_clicked_month = None # Initialize clicked month
        self.recurring_event_clicked_day = None # initalize clicked day for recurring event
        self.recurring_event_clicked_month = None  # Initialize clicked month for recurring events
        self.weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]  # Define weekdays
        #intialize 6x7 grid 
        self.date_grid = [[None for _ in range(7)] for _ in range(6)]
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="This is the Calendar Page")
        label.pack(fill="both", expand=True)

        # Frame to contain grid buttons
        calendar_frame = tk.Frame(self)
        calendar_frame.pack()

        # Calculate the weekday index for the first day of the month
        first_day = (calendar.weekday(self.current_year, self.current_month, 1) + 1) % 7

        # Adjust weekday labels based on the calculated index
        adjusted_weekdays = self.weekdays[first_day:] + self.weekdays[:first_day]

        # Weekday labels at the top
        for col, weekday in enumerate(adjusted_weekdays):
            weekday_label = tk.Label(calendar_frame, text=weekday)
            weekday_label.grid(row=0, column=col)

        # Create a grid of buttons for each day of the month
        self.buttons = []  # Store buttons in a list
        for row in range(1, 7):  # Rows for calendar grid (up to 6 rows)
            button_row = []
            for col in range(7):  # Columns for days of the week
                day_button = tk.Button(calendar_frame, text="", width=3, height=1)
                day_button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(day_button)
                #bind dialog method to button
                # 'bind' method in tkinter to bind day button and trigger when mouse button 1 is clicked
                # lambda is anonymous unnamed function _ is placeholder
                day_button.bind("<Button-1>", lambda _, col=col, row=row: self.show_event_dialog(col, row))
            self.buttons.append(button_row)
        # button for creating a recurring event
        recurring_event_button = tk.Button(self, text="Create Recurring Event", command=self.create_recurring_event)
        recurring_event_button.pack()

        # Creating arrow frames
        arrow_frame = tk.Frame(self)
        arrow_frame.pack()

        # Arrows for month navigation
        left_arrow = tk.Button(arrow_frame, text="<", command=self.prev_month)
        left_arrow.grid(row=0, column=0)
        right_arrow = tk.Button(arrow_frame, text=">", command=self.next_month)
        right_arrow.grid(row=0, column=6)

        # Initial month label
        self.month_label = tk.Label(arrow_frame, text="")
        self.update_month_label()
        self.month_label.grid(row=0, column=3)

        # Initialize the calendar grid
        self.update_calendar_grid()

    def prev_month(self):
        # Change to the previous month
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.clicked_day = None #reset clicked day
        self.clicked_month = None #reset clicked month
        self.update_month_label() 
        self.update_calendar_grid()

        # display updated values for debugging
        print(f"Before: current month = {self.current_month}, current year = {self.current_year}")

    def next_month(self):
        # Change to the next month
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.clicked_day = None #reset clicked day
        self.clicked_month = None #reset clicked month
        self.update_month_label()
        self.update_calendar_grid()

        
        # display updated values for debugging
        print(f"After: current month = {self.current_month}, current year = {self.current_year}")

    def update_month_label(self):
        # Update the month label with the current month and year
        month_name = calendar.month_name[self.current_month]
        self.month_label.config(text=f"{month_name} {self.current_year}")

    def update_calendar_grid(self):
        # Clear existing text on all buttons and reset the date_grid
        self.date_grid = [[None for _ in range(7)] for _ in range(6)]
        for button_row in self.buttons:
            for button in button_row:
                button.config(text="")

        # Calculate the dates for the current month
        cal = calendar.monthcalendar(self.current_year, self.current_month)

        # Debugging: Print first_day and adjusted_weekdays
        first_day = (calendar.weekday(self.current_year, self.current_month, 1) + 1) % 7
        adjusted_weekdays = self.weekdays[first_day:] + self.weekdays[:first_day]
        print("first day:", first_day)
        print("adjusted weekday", adjusted_weekdays)

        for row_num, week in enumerate(cal):
            for col_num, day in enumerate(week):
                if day != 0:
                    print(f"Row: {row_num}, Col: {col_num}, Day: {day}, Year: {self.current_year}, Month: {self.current_month}")
                    # Update the text on the corresponding button
                    button = self.buttons[row_num][col_num]
                    button.config(text=str(day))

                    # Store the date directly in the date_grid
                    self.date_grid[row_num][col_num] = datetime.date(self.current_year, self.current_month, day)

    def create_recurring_event(self):
        # Create a new window for recurring event settings
        recurring_event_dialog = tk.Toplevel(self)
        recurring_event_dialog.title("Recurring Event Settings")

        # Widget for selecting weekdays
        weekday_label = tk.Label(recurring_event_dialog, text="Select Weekdays:")
        weekday_label.pack()

        selected_weekdays = []
        weekday_checkbox = []

        for day in self.weekdays:
            # Represent if the box is selected
            var = tk.IntVar()
            # Check box with the weekday's name as a label
            checkbox = tk.Checkbutton(recurring_event_dialog, text=day, variable=var)
            checkbox.pack()
            # Append to the tuple weekday name and var to checkboxes
            weekday_checkbox.append((day, var))

        # Widget for specifying the number of weeks
        weeks_label = tk.Label(recurring_event_dialog, text="Number of repeating weeks")
        weeks_label.pack()
        # Allow the user to input the number of weeks
        weeks_entry = tk.Entry(recurring_event_dialog)
        weeks_entry.pack()

        # Button to confirm
        create_button = tk.Button(recurring_event_dialog, text="Create Recurring Event", command=lambda: self.add_recurring_event(weekday_checkbox, weeks_entry))
        create_button.pack()

    def add_recurring_event(self, weekday_checkbox, weeks_entry):
        # Extract selected weekday by checking if var is 1 (1 if it has been checked)
        selected_weekdays = [day for day, var in weekday_checkbox if var.get() == 1]

        # No weekdays selected
        if not selected_weekdays:
            tk.messagebox.showerror("Error", "Please select at least one weekday")
            return

        # Get the number of weeks
        try:
            num_weeks = int(weeks_entry.get())
        except ValueError:
            # Invalid input
            tk.messagebox.showerror("Error", "Invalid input for the number of weeks")
            return

        # Get the event details
        event_title = tk_simpledialog.askstring("Event Details", "Enter Event Title")
        if not event_title:
            return

        event_description = tk_simpledialog.askstring("Event Details", "Enter Event Description")
        event_start_time = tk_simpledialog.askstring("Event Details", "Enter Event Start Time (HH:MM)")
        event_end_time = tk_simpledialog.askstring("Event Details", "Enter Event End Time (HH:MM)")

        if not event_start_time:
            return

        # Calculate the start date
        start_date = datetime.date(self.current_year, self.current_month, self.single_event_clicked_day)
        
        # Create events for selected weekdays and number of weeks
        for weekday in selected_weekdays:
            # Find the index of the selected weekday
            weekday_index = self.weekdays.index(weekday)
            # Calculate the date of the first occurrence of the selected weekday
            first_occurrence_date = start_date + datetime.timedelta(days=(weekday_index - start_date.weekday() + 7) % 7)
            # Create events for the specified number of weeks
            for i in range(num_weeks):
                # Calculate the event date
                event_date = first_occurrence_date + datetime.timedelta(weeks=i)
                # Combine event date and time into datetime objects
                event_datetime = datetime.datetime.strptime(f"{event_date} {event_start_time}", "%Y-%m-%d %H:%M")
                event_end_datetime = datetime.datetime.strptime(f"{event_date} {event_end_time}", "%Y-%m-%d %H:%M")
                # Call your existing add_event function to create events
                self.add_event(event_title, event_description, event_datetime, event_end_datetime)

    def show_event_dialog(self, col, row):
        # Get the date associated with the clicked button from the date_grid
        event_date = self.date_grid[row - 1][col]

        if event_date:
            # Update the clicked day and month attributes for single-day events
            self.single_event_clicked_day = event_date.day
            self.single_event_clicked_month = event_date.month
            print(f"Clicked Day: {self.single_event_clicked_day}")
            print(f"Clicked Month: {self.single_event_clicked_month}")
            # Reset recurring event attributes
            self.recurring_event_clicked_day = None
            self.recurring_event_clicked_month = None

            # Pop up window for adding or deleting events
            event_popup = tk.Toplevel(self)
            event_popup.title(f"Events for {event_date}")

            # Add event
            add_event_button = tk.Button(event_popup, text="Add Event", command=self.add_event_popup)
            add_event_button.pack()

            # Delete event
            delete_event_button = tk.Button(event_popup, text="Delete Event", command=self.delete_event_popup)
            delete_event_button.pack()

    def add_event_popup(self):
        if self.single_event_clicked_day is not None and self.single_event_clicked_month is not None:
            print(f"Adding event for Day: {self.single_event_clicked_day}, Month: {self.single_event_clicked_month}")
            # Show add event dialog for single-day events
            event_title = tk_simpledialog.askstring("Event Details", f"Enter Event Title for {self.single_event_clicked_day}/{self.single_event_clicked_month}:")
            if event_title:
                event_description = tk_simpledialog.askstring("Event Details", "Enter Event Description:")
                event_start_time = tk_simpledialog.askstring("Event Details", "Enter Event Time (HH:MM):")
                event_end_time = tk_simpledialog.askstring("Event Details", "Enter Event end time (HH:MM)")
                if event_start_time:
                    # Format the month as a two-digit string
                    formatted_month = str(self.single_event_clicked_month).zfill(2)
                    # Combine event date and time into datetime object
                    event_datetime = datetime.datetime.strptime(
                        f"{self.current_year}-{formatted_month}-{self.single_event_clicked_day} {event_start_time}",
                        "%Y-%m-%d %H:%M"
                    )
                    event_end_datetime = datetime.datetime.strptime(
                        f"{self.current_year}-{formatted_month}-{self.single_event_clicked_day} {event_end_time}",
                        "%Y-%m-%d %H:%M"
                    )
                    self.add_event(event_title, event_description, event_datetime, event_end_datetime)
        else:
            # Show an error message if the clicked day and month are not set
            tk.messagebox.showerror("Error", "Please select a day on the calendar first.")

    def delete_event_popup(self):
        # Get the event title from the user
        event_title = tk_simpledialog.askstring("Event Details", "Enter Event Title for Event you want to delete")
        if event_title:
            # Call the delete_event function without the event_date argument
            self.delete_event(event_title)

    # Function to create an event
    def add_event(self, event_title, event_description, event_datetime, event_end_datetime):
        # retrieve event details from the user
        event = {
            'summary': event_title,
            'description': event_description,
            'start': {
                'dateTime': event_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': event_end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'America/Edmonton',
            },
        }

        # Print for debugging
        print("Clicked Day:", self.single_event_clicked_day)
        print("Clicked Month:", self.single_event_clicked_month)
        print("Event Start DateTime:", event_datetime)
        print("Event End DateTime:", event_end_datetime)

        try:
            # use google calendar api to create event
            event = calendar_service.events().insert(calendarId='primary', body=event).execute()

            # display a confirmation message to the user
            print(f'Event created: {event.get("htmlLink")}')
        except Exception as e:
            print(f"Error creating event:", (e))
            # print full traceback for debugging
            traceback.print_exc()
        else:
            print("Added successfully")
            
                
    def delete_event(self, event_title):
        try:
            # Retrieve events for the selected date
            events = calendar_service.events().list(calendarId='primary').execute()
            for event in events.get('items', []):
                # Check if the title matches
                if event['summary'] == event_title:
                    # Retrieve date from the API and convert to Python datetime
                    event_datetime = datetime.datetime.fromisoformat(event['start']['dateTime']).date()
                    # Compare the event's date (without time) to the specified date
                    if event_datetime == datetime.date(self.current_year, self.single_event_clicked_month, self.single_event_clicked_day):
                        # Delete the event with the specified ID
                        calendar_service.events().delete(calendarId='primary', eventId=event['id']).execute()
                        print(f'Event with title "{event_title}" deleted successfully')
                        return
            print(f'Event with title "{event_title}" not found')
        except Exception as e:
            print("An error has occurred", (e))