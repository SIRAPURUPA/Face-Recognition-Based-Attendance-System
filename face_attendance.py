# face_attendance.py
import os
import pickle
import cv2
import cvzone
import numpy as np
import face_recognition
import pandas as pd
from datetime import datetime
from attendance_utils import mark_attendance, mark_absentees, show_attendance_table

# Webcam config
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load background
imgBg = cv2.imread('Resources/background.png')

# Load encodings
with open('EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)

studentIds = [str(id) for id in studentIds]
print("✅ Updated Student IDs:", studentIds)
print("✅ Encoded Files Loaded")

# Output file path
timestamp = datetime.now().strftime("%d-%m-%Y_%I-%M %p")
os.makedirs("attendance_sessions", exist_ok=True)
attendance_file = os.path.join("attendance_sessions", f"Attendance_{timestamp}.xlsx")

# Save path to open later
with open("Resources/Attendance/last_session.txt", "w") as f:
    f.write(attendance_file)

# Draw info box
def draw_student_id(img, student_id="", known=True):
    box = (828, 64, 374, 593)
    cv2.rectangle(img, (808, 44), (1222, 677), (187, 123, 247), cv2.FILLED)
    cv2.rectangle(img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 255, 255), cv2.FILLED)
    def draw_centered(text, y_offset):
        (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 1.0, 2)
        x = box[0] + (box[2] - w) // 2
        y = box[1] + (box[3] // 2) + y_offset
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 64, 200), 2)
    if known:
        draw_centered("KNOWN FACE", -40)
        draw_centered("DETECTED", 0)
        draw_centered(student_id, 60)
    else:
        draw_centered("UNKNOWN", -30)
        draw_centered("FACE", 30)

frame_skip, frame_count = 2, 0
marked_students = set()

try:
    while True:
        success, img = cap.read()
        frame_count += 1

        if frame_count % frame_skip == 0:
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faces = face_recognition.face_locations(imgS)
            encodes = face_recognition.face_encodings(imgS, faces) if faces else []

            imgBg[162:642, 55:695] = img

            for encodeFace, faceLoc in zip(encodes, faces):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                if matches and len(faceDis) > 0:
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:
                        student_id = studentIds[matchIndex]
                        print("✅ Known Face Detected:", student_id)

                        if student_id not in marked_students:
                            marked_students.add(student_id)
                            mark_attendance(student_id, attendance_file)

                        draw_student_id(imgBg, student_id)
                    else:
                        draw_student_id(imgBg, known=False)
                else:
                    draw_student_id(imgBg, known=False)

                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
                imgBg = cvzone.cornerRect(imgBg, bbox, rt=0)

            cv2.imshow("Face Attendance", imgBg)

        if cv2.waitKey(1) & 0xFF == 27:
            print("\n🛑 ESC pressed. Exiting gracefully...")
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    mark_absentees(studentIds, attendance_file)
    show_attendance_table(attendance_file)
