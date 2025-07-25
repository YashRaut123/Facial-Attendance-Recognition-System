import cv2
import pickle
import numpy as np
import os

# Create the 'data' folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Load or initialize the data storage
if 'names.pkl' in os.listdir('data/'):
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
else:
    names = []

if 'faces_data.pkl' in os.listdir('data/'):
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
else:
    faces = np.empty((0, 50 * 50 * 3))  # Initialize an empty array to store faces

# Load the face detection model
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def capture_faces(name):
    """Capture 100 face samples for a given user."""
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("Error: Unable to access the camera.")
        return None
    
    faces_data = []
    i = 0

    while True:
        ret, frame = video.read()
        if not ret:
            print("Error: Unable to read from the camera.")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = facedetect.detectMultiScale(gray, 1.3, 5)

        # Check if any faces are detected before trying to unpack
        if len(faces_detected) > 0:
            for (x, y, w, h) in faces_detected:
                crop_img = frame[y:y+h, x:x+w, :]
                resized_img = cv2.resize(crop_img, (50, 50))
                
                # Collect face data every 10 frames
                if len(faces_data) < 100 and i % 10 == 0:
                    faces_data.append(resized_img)

                i += 1

                # Display captured faces and bounding box
                cv2.putText(frame, f'Collected: {len(faces_data)}', (50, 50), 
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

        cv2.imshow("Face Capture", frame)

        # Break the loop if 'q' is pressed or 100 faces have been captured
        k = cv2.waitKey(1)
        if k == ord('q') or len(faces_data) == 100:
            break

    video.release()
    cv2.destroyAllWindows()

    # Process the face data
    if len(faces_data) == 0:
        print("No faces were captured.")
        return None
    
    faces_data = np.asarray(faces_data)
    faces_data = faces_data.reshape(len(faces_data), -1)

    return faces_data

def save_data(new_faces_data, new_name):
    """Append new faces and corresponding names to the dataset and save."""
    global faces, names

    if new_faces_data is None:
        print("No data to save.")
        return

    # Add the captured face data and name to the existing dataset
    faces = np.append(faces, new_faces_data, axis=0)
    names = names + [new_name] * len(new_faces_data)

    # Save the updated names and face data
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

def main():
    while True:
        # Ask the user to input their name or quit
        name = input("Enter your name (or type 'exit' to quit): ")
        if name.lower() == 'exit':
            print("Exiting the program.")
            break
        
        # Capture faces for the entered name
        print(f"Collecting faces for {name}...")
        new_faces_data = capture_faces(name)
        
        # Save the new data
        save_data(new_faces_data, name)
        print(f"Data for {name} has been saved.")

if __name__ == "__main__":
    main()
