Local Attendance Logger

A simple desktop application to log employee attendance on Ubuntu (or other platforms) using Python and Tkinter. The application lets employees record their work start and end times locally, storing data in a CSV file. It also includes a GUI feature to view logged attendance records in a table format.

Features

- User-friendly GUI with Tkinter
- Login and Logoff buttons to mark start and end of work
- Automatically captures the system date and time for accurate logging
- Stores attendance data locally in a CSV file (`attendance_log.csv`)
- "Show Logs" button to view attendance records in a scrollable table
- Simple and lightweight, with no external dependencies except Python standard libraries

Requirements

- Python 3.x
- Tkinter (usually pre-installed with Python)
- CSV module (part of Python standard library)
- Compatible with Ubuntu and other OS with Python and GUI support

Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/local-attendance-logger.git
   ```
2. Change directory:
   ```bash
   cd local-attendance-logger
   ```

3. (Optional) Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Run the script:
   ```bash
   python3 attendance_logger.py
   ```

Usage

- Enter your employee name in the input box.
- Click **Login** when starting work.
- Click **Logoff** when ending work.
- To view all attendance records, click **Show Logs**.
- Attendance logs are saved in the `attendance_log.csv` file in the same directory.

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

License

This project is licensed under the MIT License. See the `LICENSE` file for details.

Author

Neeraj
neerajpm95@gmail.com

