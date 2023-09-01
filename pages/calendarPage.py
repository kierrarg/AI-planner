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
        self.clicked_day = None # Initialize clicked day
        self.clicked_month = None # Initialize clicked month
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="This is the Calendar Page")
        label.pack(fill="both", expand=True)

        # Frame to contain grid buttons
        calendar_frame = tk.Frame(self)
        calendar_frame.pack()

        # List of weekday labels
        self.weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        # Calculate the weekday index for the first day of the month
        first_day = calendar.weekday(self.current_year, self.current_month, 1)

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

    def update_month_label(self):
        # Update the month label with the current month and year
        month_name = calendar.month_name[self.current_month]
        self.month_label.config(text=f"{month_name} {self.current_year}")

    def update_calendar_grid(self):
        # Clear existing text on all buttons
        for button_row in self.buttons:
            for button in button_row:
                button.config(text="")

        # Calculate the dates for the current month
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        for row_num, week in enumerate(cal):
            for col_num, day in enumerate(week):
                if day != 0:
                    # Update the text on the corresponding button
                    button = self.buttons[row_num][col_num]
                    button.config(text=str(day))

    def create_recurring_event(self):
        # dialog for recurring events
        # create new window
        recurring_event_dialog = tk.Toplevel(self)
        recurring_event_dialog.title("Recurring Event Settings")

        # widget for selecting weekdays
        weekday_label = tk.Label(recurring_event_dialog, text="Select Weekdays:")
        weekday_label.pack()

        selected_weekdays = []
        weekday_checkbox = []

        for day in self.weekdays:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(recurring_event_dialog, text=day, variable=var)
            checkbox.pack()
            weekday_checkbox.append((day, var))

        # widget for specifying number of weeks
        weeks_label = tk.Label(recurring_event_dialog, text="Number of repeating weeks")
        weeks_label.pack()

        weeks_entry = tk.Entry(recurring_event_dialog)
        weeks_entry.pack()

        # button to confirm
        create_button = tk.Button(recurring_event_dialog, text="Create Recurring Event", command=lambda: self.add_recurring_event(weekday_checkbox, weeks_entry))
        create_button.pack()


    def show_event_dialog(self, col, row):
        # get text (day number) displayed on clicked button
        day_text = self.buttons[row][col]["text"]

        if day_text:
            # convert to int
            clicked_day = int(day_text)
            clicked_month = self.current_month  # Update clicked_month attribute


            # calculate weekday index for first day box in month
            first_day = datetime.date(self.current_year, self.current_month, 1).weekday()

            #calculate event date based on selected day + weekday index of first day of month
            days_to_add = (row - 1) * 7 + col - first_day
            event_date = datetime.date(self.current_year, self.current_month, 1) + datetime.timedelta(days=days_to_add)

            #update label of button to match day number
            self.buttons[row][col].config(text=str(clicked_day))

            # pop up window for adding or deleting events
            event_popup = tk.Toplevel(self)
            event_popup.title(f"Events for {event_date}")

            # add event
            add_event_button = tk.Button(event_popup, text="Add Event", command=lambda: self.add_event_popup(event_date, clicked_day, clicked_month))
            add_event_button.pack()

            # delete event
            delete_event_button = tk.Button(event_popup, text="Delete Event", command=lambda: self.delete_event_popup(event_date))
            delete_event_button.pack()


    def add_event_popup(self, event_date, clicked_day, clicked_month):
        # show add event dialog
        event_title = tk_simpledialog.askstring("Event Details", f"Enter Event Title for {event_date}:")
        if event_title:
            event_description = tk_simpledialog.askstring("Event Details", "Enter Event Description:")
            event_start_time = tk_simpledialog.askstring("Event Details", "Enter Event Time (HH:MM):")
            event_end_time = tk_simpledialog.askstring("Event Details", "Enter Event end time (HH:MM)")
            if event_start_time:
                # combine event date and time into datetime object
                event_datetime = datetime.datetime.strptime(f"{event_date} {event_start_time}", "%Y-%m-%d %H:%M")

                event_end_datetime = datetime.datetime.strptime(f"{event_date} {event_end_time}", "%Y-%m-%d %H:%M")

                # Update clicked_day and clicked_month attributes
                self.clicked_day = clicked_day
                self.clicked_month = clicked_month

                self.add_event(event_title, event_description, event_datetime, event_end_datetime)

    def delete_event_popup(self, event_date):
        # get title of event we want to delete
        event_title = tk_simpledialog.askstring("Event Details", f"Enter Event Title for Event you want to delete")
        if event_title:
            self.delete_event(event_title, event_date)


    def add_event(self, event_title, event_description, event_datetime, event_end_datetime):
        if self.clicked_day is not None and self.clicked_month is not None:
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

            try:
                # use google calendar api to create event
                event = calendar_service.events().insert(calendarId='primary', body=event).execute()

                # display a confirmation message to the user
                print(f'Event created: {event.get("htmlLink")}')
            except Exception as e:
                print(f"Error creating event:", (e))
                #print full traceback for debugging
                traceback.print_exc()

    def delete_event(self, event_title, event_date):
        try:
            # retrieve event for selected date
            events = calendar_service.events().list(calendarId='primary').execute()
            for event in events.get('items', []):
                # check if title matches
                if event['summary'] == event_title:
                    # retrieve date and time from api and convert to python datetime
                    event_datetime = datetime.datetime.fromisoformat(event['start']['dateTime'])
                    # delete event with specified id
                    if event_datetime.date() == event_date:
                        calendar_service.events().delete(calendarId='primary', eventId=event['id']).execute()
                        print(f'Event with title "{event_title} deleted successfully')
                        return
            print(f'Event with title "{event_title}" not found')
        except Exception as e:
            print("An error has occured", (e))