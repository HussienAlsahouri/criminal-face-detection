import sys
import face_recognition
import pygame
import os
import cv2
import numpy as np
import math
import tensorflow as tf
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import concurrent.futures
import datetime
from PIL import Image
from PIL.ExifTags import TAGS


pygame.mixer.init()
sound = pygame.mixer.Sound(r'C:\Users\Saed\PycharmProjects\pythonProject3\pythonProject2\Alarms\wrong-answer-129254.mp3')

# Helper function to preprocess face images
def preprocess_face(face_image):
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = cv2.resize(face_image, (128, 128))
    face_image = np.reshape(face_image, (128, 128, 1))
    face_image = face_image / 255.0
    return face_image

# Class for face recognition
class FaceRecognition:
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()
        self.load_model()

    def encode_faces(self):
        for image in os.listdir('images'):
            face_image = face_recognition.load_image_file(f"images/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def load_model(self):
        self.model = tf.keras.models.load_model('face_recognition_model.h5')

    def preprocess_face(self, face_image):
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_image = cv2.resize(face_image, (128, 128))
        face_image = np.reshape(face_image, (128, 128, 1))
        face_image = face_image / 255.0
        return face_image

    def predict_face(self, face_encoding):
        processed_encoding = self.preprocess_face(face_encoding)
        print(self.model.input_shape)
        print(processed_encoding.shape)
        predictions = self.model.predict(np.array([processed_encoding]))
        # Perform further processing on the predictions to determine the recognized face
        # ...

    def detect_faces_caffe(self, frame):
        net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000_fp16.caffemodel')

        # Resize the frame to 300x300 pixels for face detection
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)

        # Perform face detection
        detections = net.forward()

        face_locations = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections
            if confidence > 0.2:
                # Get the coordinates of the bounding box
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")

                # Convert the coordinates to the format expected by face_recognition
                face_location = (startY, endX, endY, startX)
                face_locations.append(face_location)

        return face_locations

    def process_frame(self, frame):
        # Perform face detection and recognition for each frame
        face_locations_caffe = self.detect_faces_caffe(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations_caffe)

        face_names = []
        for face_location, face_encoding in zip(face_locations_caffe, face_encodings):
            # ... (your existing face recognition logic)
            # Append the results to face_names list

            return face_locations_caffe, face_names

    def run_recognition(self):
        # Open the webcam for video capture
        video_capture = cv2.VideoCapture(1)  # 0 corresponds to the default camera (usually the built-in webcam)

        # Set the desired window width and height
        window_width = 1920
        window_height = 1080

        # Create a named window with the specified width and height
        cv2.namedWindow('Face Recognition', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Face Recognition', window_width, window_height)

        frame_count = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            while True:
                ret, frame = video_capture.read()

                # Only process every other frame to save time
                if self.process_current_frame:
                    if frame_count % 5 == 0:
                        future = executor.submit(self.process_frame, frame)
                        # Use the Caffe model for face detection
                        face_locations_caffe = self.detect_faces_caffe(frame)

                        self.face_locations = face_locations_caffe
                        self.face_encodings = face_recognition.face_encodings(frame, self.face_locations)

                        self.face_names = []
                        for face_location, face_encoding in zip(self.face_locations, self.face_encodings):
                            # Check the size of the face bounding box
                            top, right, bottom, left = face_location
                            face_height = bottom - top
                            face_width = right - left

                            # Set a minimum threshold for face size (adjust this value as needed)
                            min_face_height_threshold = 0.8  # Adjust this value as needed
                            min_face_width_threshold = 0.8  # Adjust this value as needed

                            # Initialize name and confidence
                            name = " "
                            confidence = " "

                            if face_height >= min_face_height_threshold and face_width >= min_face_width_threshold:
                                # Process the face only if it's larger than the threshold
                                # See if the face is a match for the known face(s)
                                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                                if True in matches:
                                    # Calculate the face distances to find the best match
                                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                                    if len(face_distances) > 0:
                                        # Find the index of the face with the minimum distance
                                        best_match_index = np.argmin(face_distances)

                                        if matches[best_match_index]:
                                            name = self.known_face_names[best_match_index].split(".")[0]
                                            confidence = self.face_confidence(face_distances[best_match_index])

                                            # Record the date and time of the match
                                            match_time = datetime.datetime.now()

                                            # Create a folder for the image if it doesn't exist
                                            image_folder = os.path.join('matches', name)
                                            if not os.path.exists(image_folder):
                                                os.makedirs(image_folder)


                                            # Extract the current time and format it
                                            #current_time = match_time.strftime("%Y%m%d%H%M%S")

                                            # Take a screenshot of the frame
                                            screenshot = frame.copy()
                                            screenshot_filename = os.path.join(image_folder, f"{name}_{confidence}.jpg")
                                            cv2.imwrite(screenshot_filename, screenshot)
                                            # Play the sound
                                            sound.play()

                                            # Print or save the date and time of the match
                                           # print(f"Matched {name} at {match_time}")


                            self.face_names.append(f'{name} ({confidence})')

                # Display the results
                for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                    # Create the frame with the name
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    # Calculate the text position
                    text_width, text_height = cv2.getTextSize(name, cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)[0]
                    text_x = left + int((right - left - text_width) / 2)
                    text_y = bottom - 6

                    # Draw the text
                    cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

                # Resize the frame to the desired window width and height
                resized_frame = cv2.resize(frame, (window_width, window_height))

                # Display the resulting image
                cv2.imshow('Face Recognition', resized_frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) == ord('q'):
                    break

                frame_count += 1

        # Release the webcam and close all OpenCV windows
        video_capture.release()
        cv2.destroyAllWindows()

    @staticmethod
    def face_confidence(face_distance, face_match_threshold=0.8):
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_val * 100, 2)) + '%'
        else:
            value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + '%'

if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
