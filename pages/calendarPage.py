import tkinter as tk
from tkinter import simpledialog
import calendar

class CalendarPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#ADD8E6")
        self.current_month = 8  # Set the initial month (e.g., August)
        self.current_year = 2023  # Set the initial year
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="This is the Calendar Page")
        label.pack(fill="both", expand=True)

        # Frame to contain grid buttons
        calendar_frame = tk.Frame(self)
        calendar_frame.pack()

        # List of weekday labels
        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        # Calculate the weekday index for the first day of the month
        first_day = calendar.weekday(self.current_year, self.current_month, 1)

        # Adjust weekday labels based on the calculated index
        adjusted_weekdays = weekdays[first_day:] + weekdays[:first_day]

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
            self.buttons.append(button_row)

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
        self.update_month_label()
        self.update_calendar_grid()

    def next_month(self):
        # Change to the next month
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
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
