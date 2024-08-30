import math
from sklearn import neighbors
import os
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder

# Define allowed image file extensions
allowed_extensions = {'png', 'jpg', 'jpeg', 'JPG'}

# Function to check if a given directory exists in the training directory
def is_directory(training_dir, class_dir):
    return os.path.isdir(os.path.join(training_dir, class_dir))

# Function to train a K-Nearest Neighbors (KNN) classifier for face recognition
def training_knn(training_dir, model_dest_path=None, n_neighbors=None, knn_algo='ball_tree'):
    X = []  # List to hold face encodings (features)
    y = []  # List to hold corresponding labels (person names)

    # Loop through each person (class) in the training directory
    for class_dir in os.listdir(training_dir):
        if not is_directory(training_dir, class_dir):
            continue

        # Loop through each image file of the person
        directory_path = os.path.join(training_dir, class_dir)
        for img_path in image_files_in_folder(directory_path):
            # Load the image
            image = face_recognition.load_image_file(img_path)
            # Find face locations in the image
            face_bounding_boxes = face_recognition.face_locations(image)

            # Skip images with no faces or multiple faces
            if len(face_bounding_boxes) != 1:
                #print(f"{img_path} didn't train")
                continue
            else:
                # Encode the face found in the image and add it to the training set
                X.append(face_recognition.face_encodings(
                    image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determine the optimal number of neighbors if not provided
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))

    # Train the KNN classifier with the collected face encodings
    knn_clf = neighbors.KNeighborsClassifier(
        n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN model to a file if a path is provided
    if model_dest_path is not None:
        with open(model_dest_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf

# Main function to train the KNN classifier
def main():
    print("Training KNN classifier")
    # Train the KNN classifier using images in the "image dataset" directory
    classifier = training_knn(
        "image dataset", model_dest_path="trained_knn_model.clf", n_neighbors=2)
    print("Training complete!")

if __name__ == "__main__":
    main()  # Run the main function if the script is executed
