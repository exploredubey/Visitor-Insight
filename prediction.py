import json
import cv2
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
import numpy as np
from data_preparation import capture_and_save_image
import telegramNotification as tl3
from datetime import datetime, time

# Allowed file extensions for image formats
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG', "pgm"}

# Function to load the KNN classifier from a file
def get_knn_classifier(model_path):
    with open(model_path, 'rb') as f:
        knn_classifier = pickle.load(f)
    return knn_classifier

# Function to get the matches by comparing face encodings with the KNN classifier
def get_matches(knn_classifier, distance_threshold, face_locations, faces_encodings):
    closest_distances = knn_classifier.kneighbors(
        faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <=
                   distance_threshold for i in range(len(face_locations))]
    return are_matches

# Function to predict the identity of faces in a frame using KNN
def predict_knn(frame, knn_classifier=None, model_path=None, distance_threshold=0.5):
    if knn_classifier is None and model_path is None:
        raise Exception("No KNN classifier passed")

    # Load a trained KNN model (if one was passed in)
    if knn_classifier is None:
        knn_classifier = get_knn_classifier(model_path)

    # Detect face locations in the frame
    face_locations = face_recognition.face_locations(frame)

    # Return an empty list if no faces are detected
    if len(face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(
        frame, known_face_locations=face_locations)

    # Get the best matches
    are_matches = get_matches(
        knn_classifier, distance_threshold, face_locations, faces_encodings)

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_classifier.predict(faces_encodings), face_locations, are_matches)]

# Function to draw prediction labels on the image
def show_prediction_labels_on_image(frame, predictions):
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # Enlarge the predictions for the full-sized image.
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2
        # Draw a box around the face
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Encode name to avoid issues with non-UTF-8 text
        name = name.encode("UTF-8")

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10),
                       (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5),
                  name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory.
    del draw
    # Convert the PIL image back to OpenCV format for display
    opencvimage = np.array(pil_image)
    return opencvimage

# Function to load roles from a JSON file
def get_roles_from_json(json_file):
    with open(json_file, "r") as f:
        roles_dict = json.load(f)
    return roles_dict

# Function to get the role of a person based on their name
def get_role(name):
    json_file = "roles.json"
    if name == "unknown":
        return None
    if os.path.exists(json_file):
        roles_dict = get_roles_from_json(json_file)
    else:
        return None

    return roles_dict[name]

# Function to capture and save an image from the webcam
def get_image():
    webcam = cv2.VideoCapture("abhishek.mp4")
    filename = capture_and_save_image("unknown", 1, webcam)
    webcam.release()
    cv2.destroyAllWindows()
    return filename

# Function to handle the case where an unknown person is detected
def handle_unknown_person():
    image = get_image()
    text = 'Hi! Unknown Person at the door. Do you want to Allow / Deny?'
    tl3.messaging(text, image)

# Function to handle the case where a known person is detected within the allowed time
def handle_known_person(name, starttime, endtime):
    nowtime = datetime.now().time()

    if time(starttime) <= nowtime <= time(endtime):
        tl3.telegram_bot_sendtext(
            f"Known person {name} at door. Letting them in.")
    else:
        tl3.known_person_wrong_time(
            f"Known person {name} at door but wrong timing. Allow/Deny?")

# Function to handle the case where a family member is detected
def handle_family_person(predicted_name):
    tl3.telegram_bot_sendtext(f"{predicted_name} has been let into house")

# Main function to run the face recognition system
def main():
    process_this_frame = 0
    print('Setting cameras up...')

    cap = cv2.VideoCapture("abhishek.mp4")
    model_path = "trained_knn_model.clf"

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Resize the frame for faster processing
        img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        process_this_frame += 1

        predictions = predict_knn(img, model_path=model_path)
        if process_this_frame % 30 == 0:
            predictions = predict_knn(img, model_path=model_path)
            try:
                print(predictions[0][0])
            except IndexError:
                continue
            predicted_name = predictions[0][0]
            cap.release()
            cv2.destroyAllWindows()

            if predicted_name == 'unknown':
                handle_unknown_person()
                break

            role = get_role(predicted_name)
            role, starttime, endtime = role[0], role[1], role[2]
            if role != "Family":
                handle_known_person(predicted_name, starttime, endtime)
                break
            else:
                handle_family_person(predicted_name)
                break

        # Display the frame with prediction labels
        frame = show_prediction_labels_on_image(frame, predictions)
        cv2.imshow('camera', frame)
        if ord('q') == cv2.waitKey(10):
            break


if __name__ == "__main__":
    main()
