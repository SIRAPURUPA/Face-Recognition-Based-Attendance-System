# main.py
import tkinter as tk
import subprocess
import os
import sys

python_executable = sys.executable

# Launch Add Student UI
def add_student():
    subprocess.Popen([python_executable, "add_student_ui.py"])

# Launch Face Attendance UI
def mark_attendance():
    subprocess.run([python_executable, "face_attendance.py"])

# Open Attendance Folder
def view_attendance():
    path = os.path.abspath("attendance_sessions")
    os.makedirs(path, exist_ok=True)
    os.startfile(path)

# Setup UI
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x350")
root.config(bg="#f0f0ff")

label = tk.Label(root, text="Welcome to Attendance System", font=("Helvetica", 14, "bold"), bg="#f0f0ff")
label.pack(pady=20)

tk.Button(root, text="➕ Add New Student", width=25, height=2, command=add_student, bg="#b3e5fc").pack(pady=10)
tk.Button(root, text="📷 Mark Attendance", width=25, height=2, command=mark_attendance, bg="#c8e6c9").pack(pady=10)
tk.Button(root, text="📁 View Attendance Files", width=25, height=2, command=view_attendance, bg="#ffe082").pack(pady=10)

root.mainloop()
