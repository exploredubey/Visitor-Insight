import cv2
import os
import json
from datetime import time
from training import training_knn
import numpy as np
from skimage import io, img_as_ubyte
from skimage import transform as tf
from skimage.transform import rotate

# Function to apply a shear transformation to an image and save the result
def sheer_image(name, frame_num, sheer_factor, filename, ind=1):
    image = io.imread(filename)
    # Create affine transform for shearing
    afine_tf = tf.AffineTransform(shear=sheer_factor)
    # Apply the affine transform to the image
    modified = tf.warp(image, inverse_map=afine_tf)
    # Save the sheared image
    sheer_filename = f"image dataset/{name}/img{frame_num}sheer{ind}.jpg"
    io.imsave(sheer_filename, img_as_ubyte(modified))

# Function to rotate an image by a specified angle and save the result
def rotate_image(name, frame_num, rotate_factor, filename, ind=1):
    image = io.imread(filename)
    # Rotate the image by the given factor
    new_pic = rotate(image, rotate_factor)
    # Save the rotated image
    rotate_filename = f"image dataset/{name}/img{frame_num}rotate{ind}.jpg"
    io.imsave(rotate_filename, img_as_ubyte(new_pic))

# Function to capture an image from the webcam, save it, and apply transformations
def capture_and_save_image(name, frame_num, webcam):
    print(f"Capturing {name} frame {frame_num}")
    ret, frame = webcam.read()
    key = cv2.waitKey(1)

    # Define the filename for the captured image
    filename = f"image dataset/{name}/img{frame_num}.jpg"
    # Create the directory if it doesn't exist
    if not os.path.exists(f"image dataset/{name}"):
        os.makedirs(f"image dataset/{name}")

    # Save the captured image
    cv2.imwrite(filename=filename, img=frame)

    # Apply shear and rotate transformations to the captured image
    sheer_image(name, frame_num, 0.1, filename)
    rotate_image(name, frame_num, -5, filename)
    rotate_image(name, frame_num, 5, filename, 2)

    return filename

# Function to display a message on the webcam feed for a specified duration
def wait_for_some_time(webcam, text, frame_wait=100):
    for i in range(frame_wait):
        ret, frame = webcam.read()
        cv2.putText(frame, text, (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 3)
        cv2.imshow("cap", frame)
        key = cv2.waitKey(1)

# Function to capture a series of images from the webcam for a specific person
def collect_images(name, num_of_frames=4, unknown=False):
    webcam = cv2.VideoCapture("abhishek.mp4")
    counter = 0
    frames = 0
    # Display a message before starting the image collection process
    wait_for_some_time(
        webcam, "Starting process to add image to dataset.", 100)
    try:
        while True:
            # Capture and display the current frame
            ret, frame = webcam.read()
            cv2.putText(frame, "Please wait while, adding your image to database",
                        (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 3)
            cv2.imshow("cap", frame)
            key = cv2.waitKey(1)

            # Stop the process if 'q' is pressed
            if key == ord('q'):
                break
            # Capture and save an image every 40 frames
            if counter % 40 == 0:
                capture_and_save_image(name, frames, webcam)
                frames += 1

            # Stop the process after the required number of frames is captured
            if frames == num_of_frames:
                wait_for_some_time(
                    webcam, "Image added successfully. Closing now.", 150)
                break

            counter += 1
        print("DONE")
    except Exception as e:
        print("Exception occurred", e)
        pass

    # Release the webcam and close the display window
    print("Turning off camera.")
    webcam.release()
    print("Camera off.")
    print("Program ended.")
    cv2.destroyAllWindows()

# Function to register a person's role and allowed time in a JSON file
def register_person(name, role, start, end):
    json_file = "roles.json"
    # Load existing roles from the JSON file if it exists
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            roles_dict = json.load(f)
    else:
        roles_dict = {}

    # Add or update the role for the person
    roles_dict[name] = [role, start, end]

    # Save the updated roles back to the JSON file
    with open(json_file, "w") as f:
        json.dump(roles_dict, f)

# Function to process a person by collecting their images and registering their role
def process_person(name, role, start_hr, end_hr):
    # Collect images of the person using the webcam
    collect_images(name)
    # Register the person's role and allowed time
    register_person(name, role, start_hr, end_hr)

    # Train the KNN classifier with the collected images
    print("Training KNN classifier")
    classifier = training_knn(
        "image dataset", model_dest_path="trained_knn_model.clf", n_neighbors=2)
    print("Training complete!")

# Main function to input details of a person and process them
def main():
    name = input("Enter Person Name:")  # Input the person's name
    role = input("Enter person role:")  # Input the person's role
    print("Enter start hr.")
    start_hr = int(input())  # Input the start hour for access
    print("Enter end hr.")
    end_hr = int(input())  # Input the end hour for access

    # Process the person by collecting images, registering their role, and training the classifier
    process_person(name, role, start_hr, end_hr)

if __name__ == "__main__":
    main()  # Run the main function if the script is executed
