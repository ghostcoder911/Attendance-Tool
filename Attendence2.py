#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import csv
import os

CSV_FILE = 'attendance_log.csv'

def write_to_csv(name, date, start_time, end_time):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Employee Name', 'Date', 'Start Time', 'End Time'])
        writer.writerow([name, date, start_time, end_time])

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Attendance Logger")

        self.name = tk.StringVar()
        self.start_time = None

        tk.Label(root, text="Employee Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.name).grid(row=0, column=1, padx=10, pady=10)

        tk.Button(root, text="Login", width=15, command=self.login).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(root, text="Logoff", width=15, command=self.logoff).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Show Logs", width=15, command=self.show_logs).grid(row=1, column=2, padx=10, pady=10)

    def login(self):
        employee = self.name.get().strip()
        if not employee:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        if self.start_time is not None:
            messagebox.showwarning("Action Error", "Already logged in.")
            return
        self.start_time = datetime.datetime.now()
        messagebox.showinfo("Success", f"Login time recorded: {self.start_time.strftime('%H:%M:%S')}")

    def logoff(self):
        employee = self.name.get().strip()
        if not employee:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        if self.start_time is None:
            messagebox.showwarning("Action Error", "You need to login first.")
            return
        end_time = datetime.datetime.now()

        date_str = self.start_time.strftime('%Y-%m-%d')
        start_str = self.start_time.strftime('%H:%M:%S')
        end_str = end_time.strftime('%H:%M:%S')
        write_to_csv(employee, date_str, start_str, end_str)

        self.start_time = None
        messagebox.showinfo("Success", f"Logoff time recorded: {end_str}\nAttendance saved to {CSV_FILE}")

    def show_logs(self):
        try:
            if not os.path.isfile(CSV_FILE):
                messagebox.showinfo("No Data", "No attendance log file found.")
                return

            logs_window = tk.Toplevel(self.root)
            logs_window.title("Attendance Logs")
            logs_window.geometry("550x300")

            frame = tk.Frame(logs_window)
            frame.pack(fill=tk.BOTH, expand=True)

            vsb = tk.Scrollbar(frame, orient="vertical")
            vsb.pack(side='right', fill='y')

            tree = ttk.Treeview(frame,
                                columns=('Name', 'Date', 'Start Time', 'End Time'),
                                show='headings',
                                yscrollcommand=vsb.set)
            tree.heading('Name', text='Employee Name')
            tree.heading('Date', text='Date')
            tree.heading('Start Time', text='Start Time')
            tree.heading('End Time', text='End Time')

            tree.column('Name', width=150)
            tree.column('Date', width=100)
            tree.column('Start Time', width=100)
            tree.column('End Time', width=100)

            tree.pack(fill=tk.BOTH, expand=True)
            vsb.config(command=tree.yview)

            with open(CSV_FILE, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # skip header
                row_count = 0
                for row in reader:
                    if row:
                        tree.insert('', tk.END, values=row)
                        row_count += 1
                if row_count == 0:
                    messagebox.showinfo("No Entries", "No attendance records found in the CSV.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

