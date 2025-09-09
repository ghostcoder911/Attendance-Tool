#!/bin/bash
This script activates the virtual environment and runs the application.
Check if the virtual environment exists

if [ ! -d "venv" ]; then
echo "Virtual environment 'venv' not found. Please create it first:"
echo "python3 -m venv venv"
exit 1
fi
Activate the virtual environment

source venv/bin/activate
Run the Python script

echo "Starting Employee Attendance Tracker..."
python attendance_app.py

echo "Script finished."
Optional: To deactivate the venv after the script finishes, you can uncomment the line below.
deactivate
