import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import os

# --- Script Configuration ---
# You must first follow the steps in setup_instructions.md to get your credentials.
# Then, replace the following placeholders with your information.
SPREADSHEET_NAME = "Employee_Attendance"  # Updated to your specified sheet name
WORKSHEET_NAME = "Logs"
SERVICE_ACCOUNT_FILE = "service_account.json"

def get_google_sheet_client():
    """Authenticates and returns a gspread client."""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError:
        messagebox.showerror("Authentication Error", 
                             f"Error: '{SERVICE_ACCOUNT_FILE}' not found.\n"
                             f"Please follow the setup instructions to get your credentials.")
        return None
    except Exception as e:
        messagebox.showerror("Authentication Error", f"An error occurred during authentication: {e}")
        return None

class AttendanceApp(tk.Tk):
    """A Tkinter application for tracking employee attendance in Google Sheets."""
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Employee Attendance Tracker")
        self.geometry("450x350")
        self.configure(bg="#f0f2f5")

        # Define a consistent font style
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        # Attempt to connect to Google Sheets
        self.gs_client = get_google_sheet_client()
        if self.gs_client:
            try:
                self.spreadsheet = self.gs_client.open(SPREADSHEET_NAME)
                self.worksheet = self.spreadsheet.worksheet(WORKSHEET_NAME)
                self.setup_ui()
            except gspread.exceptions.SpreadsheetNotFound:
                messagebox.showerror("Spreadsheet Error", 
                                     f"Spreadsheet named '{SPREADSHEET_NAME}' not found.\n"
                                     "Please check the name or create the sheet first.")
                self.destroy()
            except gspread.exceptions.WorksheetNotFound:
                messagebox.showerror("Worksheet Error", 
                                     f"Worksheet named '{WORKSHEET_NAME}' not found.\n"
                                     "Please check the name or create the worksheet first.")
                self.destroy()
        else:
            self.destroy()

    def setup_ui(self):
        """Creates all the GUI elements."""
        # Main frame
        main_frame = tk.Frame(self, bg="#f0f2f5", padx=20, pady=20)
        main_frame.pack(expand=True)

        # Title Label
        title_label = tk.Label(main_frame, text="Attendance Tracker", font=self.title_font, bg="#f0f2f5", fg="#333")
        title_label.pack(pady=(0, 20))

        # Employee Name Input
        name_label = tk.Label(main_frame, text="Employee Name:", font=self.label_font, bg="#f0f2f5", fg="#555")
        name_label.pack()
        
        self.name_entry = tk.Entry(main_frame, width=30, font=self.label_font, bd=2, relief="groove")
        self.name_entry.pack(pady=(5, 15))

        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg="#f0f2f5")
        button_frame.pack()

        # Login Button
        login_button = tk.Button(button_frame, text="Login", font=self.button_font, command=self.login,
                                 bg="#4caf50", fg="white", activebackground="#45a049",
                                 relief="raised", bd=3, padx=10, pady=5)
        login_button.pack(side="left", padx=5)

        # Logoff Button
        logoff_button = tk.Button(button_frame, text="Logoff", font=self.button_font, command=self.logoff,
                                  bg="#f44336", fg="white", activebackground="#d32f2f",
                                  relief="raised", bd=3, padx=10, pady=5)
        logoff_button.pack(side="left", padx=5)

        # View Logs Button
        view_button = tk.Button(button_frame, text="View Logs", font=self.button_font, command=self.view_logs,
                                bg="#2196f3", fg="white", activebackground="#1e88e5",
                                relief="raised", bd=3, padx=10, pady=5)
        view_button.pack(side="left", padx=5)

        # Status Label
        self.status_label = tk.Label(main_frame, text="", font=self.label_font, bg="#f0f2f5", fg="#333")
        self.status_label.pack(pady=(20, 0))

    def update_status(self, message, color="black"):
        """Updates the status label with a message and color."""
        self.status_label.config(text=message, fg=color)
    
    def login(self):
        """Records the login time for an employee."""
        name = self.name_entry.get().strip()
        if not name:
            self.update_status("Please enter an employee name.", color="red")
            return

        try:
            # Check for existing records
            list_of_names = self.worksheet.col_values(1)
            try:
                row_index = list_of_names.index(name) + 1
            except ValueError:
                row_index = None

            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if row_index:
                # Employee already exists, update the login time
                self.worksheet.update_cell(row_index, 2, login_time)
                self.update_status(f"Login time updated for {name} at {login_time}.", color="green")
            else:
                # New employee, append a new row
                self.worksheet.append_row([name, login_time, ""])
                self.update_status(f"New entry created for {name} at {login_time}.", color="green")

        except gspread.exceptions.APIError as e:
            messagebox.showerror("API Error", f"An API error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def logoff(self):
        """Records the logoff time for an employee."""
        name = self.name_entry.get().strip()
        if not name:
            self.update_status("Please enter an employee name.", color="red")
            return

        try:
            list_of_names = self.worksheet.col_values(1)
            try:
                row_index = list_of_names.index(name) + 1
            except ValueError:
                self.update_status(f"Employee '{name}' not found. Please log in first.", color="red")
                return

            logoff_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.worksheet.update_cell(row_index, 3, logoff_time)
            self.update_status(f"Logoff time updated for {name} at {logoff_time}.", color="green")
            
        except gspread.exceptions.APIError as e:
            messagebox.showerror("API Error", f"An API error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def view_logs(self):
        """Fetches and displays all attendance logs in a new window."""
        try:
            all_records = self.worksheet.get_all_records()
            
            if not all_records:
                messagebox.showinfo("Logs", "No attendance logs found yet.")
                return

            log_window = tk.Toplevel(self)
            log_window.title("Attendance Logs")
            log_window.geometry("600x400")
            log_window.configure(bg="#f0f2f5")

            logs_text = tk.Text(log_window, wrap="word", font=("Courier", 10), bg="white")
            logs_text.pack(expand=True, fill="both", padx=10, pady=10)

            # Format and insert the header
            header = "{:<25} {:<25} {:<25}".format("Employee Name", "Login Time", "Logoff Time")
            logs_text.insert(tk.END, header + "\n")
            logs_text.insert(tk.END, "-" * 75 + "\n")
            
            # Format and insert the data
            for record in all_records:
                name = record.get("Employee Name", "")
                login = record.get("Login Time", "")
                logoff = record.get("Logoff Time", "")
                row_text = "{:<25} {:<25} {:<25}".format(name, login, logoff)
                logs_text.insert(tk.END, row_text + "\n")

            logs_text.config(state=tk.DISABLED) # Make the text widget read-only

        except gspread.exceptions.APIError as e:
            messagebox.showerror("API Error", f"An API error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()
