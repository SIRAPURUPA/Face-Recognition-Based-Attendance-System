# attendance_utils.py
import os
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk

present_ids_today = set()

def mark_attendance(student_id, attendance_file):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    os.makedirs(os.path.dirname(attendance_file), exist_ok=True)

    if os.path.exists(attendance_file):
        df_existing = pd.read_excel(attendance_file)
    else:
        df_existing = pd.DataFrame(columns=["ID", "Status", "Date", "Time"])

    already_marked = (
        (df_existing["ID"] == student_id) & (df_existing["Date"] == date_str)
    ).any()

    if not already_marked:
        new_row = pd.DataFrame([{
            "ID": student_id,
            "Status": "Present",
            "Date": date_str,
            "Time": time_str
        }])
        df_final = pd.concat([df_existing, new_row], ignore_index=True)

        try:
            df_final.to_excel(attendance_file, index=False)
            present_ids_today.add(student_id)
            print(f"✅ Attendance marked for {student_id}")
        except PermissionError:
            print("❌ Unable to save attendance. Please close the Excel file.")
    else:
        print(f"🟡 Already marked for {student_id} today")

def mark_absentees(all_ids, attendance_file):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    if os.path.exists(attendance_file):
        df = pd.read_excel(attendance_file)
    else:
        df = pd.DataFrame(columns=["ID", "Status", "Date", "Time"])

    absentees = [sid for sid in all_ids if sid not in present_ids_today]
    for sid in absentees:
        already_marked = (
            (df["ID"] == sid) & (df["Date"] == date_str)
        ).any()
        if not already_marked:
            new_row = pd.DataFrame([{
                "ID": sid,
                "Status": "Absent",
                "Date": date_str,
                "Time": time_str
            }])
            df = pd.concat([df, new_row], ignore_index=True)

    try:
        df.to_excel(attendance_file, index=False)
    except PermissionError:
        print("❌ Please close the Excel file to save absentees.")

def show_attendance_table(file_path):
    if not os.path.exists(file_path):
        print("❌ Attendance file not found.")
        return

    df = pd.read_excel(file_path)
    print("\n📋 Attendance Table:")
    print(tabulate(df, headers='keys', tablefmt='pretty'))

    root = tk.Tk()
    root.title("Session Attendance")
    root.geometry("600x400")

    tree = ttk.Treeview(root)
    tree.pack(fill=tk.BOTH, expand=True)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    root.mainloop()
