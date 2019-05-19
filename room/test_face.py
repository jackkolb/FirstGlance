import face_recognition
import cv2


known_image = face_recognition.load_image_file("room/images/Kolb.png")
kolb_encoding = face_recognition.face_encodings(known_image)[0]



video_capture = cv2.VideoCapture(0)


