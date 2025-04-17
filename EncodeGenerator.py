import os
import cv2
import face_recognition
import pickle

# Folder with student images
path = 'Images'
images = []
student_ids = []
image_files = os.listdir(path)

for img_name in image_files:
    img = cv2.imread(os.path.join(path, img_name))
    if img is not None:
        images.append(img)
        student_ids.append(os.path.splitext(img_name)[0])  # Get ID from filename


# Function to encode faces
def find_encodings(images_list):
    encode_list = []
    for img in images_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(img)
        if boxes:
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        else:
            print("⚠️ No face found in image.")
    return encode_list


print("✅ Encoding faces...")
encode_list_known = find_encodings(images)
print("✅ Encoding complete.")

# Save encodings
with open('EncodeFile.p', 'wb') as f:
    pickle.dump((encode_list_known, student_ids), f)

print("✅ EncodeFile.p saved.")