from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

# Function to speak using SAPI.SpVoice
def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# Initialize video capture and face detection model
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load names and face data for prediction
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

# Initialize KNeighborsClassifier and fit the model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Define column names for attendance CSV
COL_NAMES = ['NAME', 'TIME']

# Ensure the Attendance folder exists
if not os.path.exists('Attendance'):
    os.makedirs('Attendance')

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    # Loop through detected faces
    for (x, y, w, h) in faces:
        # Crop, resize, and reshape the face image for prediction
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        
        # Predict the person's name using KNN
        output = knn.predict(resized_img)
        
        # Generate timestamps for attendance
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        
        # Check if attendance file for today already exists
        attendance_file = "Attendance/Attendance_" + date + ".csv"
        exist = os.path.isfile(attendance_file)
        
        # Draw rectangles and text around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        
        # Prepare attendance data
        attendance = [str(output[0]), str(timestamp)]
        
        # Show the frame with the face and label
    cv2.imshow("Frame", frame)
    
    # Check if 'o' key is pressed for marking attendance
    k = cv2.waitKey(1)
    if k == ord('o'):
        speak("Attendance Taken.")
        time.sleep(2)  # Give a short delay
        
        # Append attendance to the CSV file
        with open(attendance_file, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not exist:  # If the file doesn't exist, write the headers
                writer.writerow(COL_NAMES)
            writer.writerow(attendance)
    
    # Exit if 'q' key is pressed
    if k == ord('q'):
        break

# Release video capture and close windows
video.release()
cv2.destroyAllWindows()
