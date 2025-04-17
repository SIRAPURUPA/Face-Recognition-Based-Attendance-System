# add_student_ui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import cv2
import face_recognition
import pickle

IMAGE_FOLDER = "images"
ENCODE_FILE = "EncodeFile.p"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

selected_image_path = None

# Save image and encode
def save_image():
    student_id = entry_id.get().strip()
    if not student_id:
        messagebox.showerror("Error", "Please enter Student ID")
        return
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an image")
        return

    dest_path = os.path.join(IMAGE_FOLDER, f"{student_id}.jpg")
    shutil.copyfile(selected_image_path, dest_path)
    messagebox.showinfo("Success", f"Image saved as {student_id}.jpg")
    encode_faces()
    label_status.config(text="✅ Student added and encoded!", fg="green")

# Encoding logic
def encode_faces():
    image_files = os.listdir(IMAGE_FOLDER)
    images, student_ids = [], []

    for img_name in image_files:
        img_path = os.path.join(IMAGE_FOLDER, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
            student_ids.append(os.path.splitext(img_name)[0])

    encode_list = []
    for img in images:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb_img)
        if boxes:
            encode = face_recognition.face_encodings(rgb_img)[0]
            encode_list.append(encode)

    with open(ENCODE_FILE, 'wb') as f:
        pickle.dump((encode_list, student_ids), f)

# Browse image file
def select_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        selected_image_path = file_path
        label_selected.config(text=os.path.basename(file_path), fg="blue")

# UI
root = tk.Tk()
root.geometry("400x350")
root.title("Add Student Face")

tk.Label(root, text="Student ID:").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Select Image File:").pack(pady=5)
tk.Button(root, text="Select Image", command=select_image).pack()
label_selected = tk.Label(root, text="No image selected")
label_selected.pack()

tk.Button(root, text="Save & Encode", command=save_image).pack(pady=10)
label_status = tk.Label(root, text="")
label_status.pack()

root.mainloop()
