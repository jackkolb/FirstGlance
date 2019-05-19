import face_recognition
import cv2


def wait_for_doctor(doctor_name):

    doctor_images = {
        "Jack Kolb": "room/images/Kolb.png",
        "Sumanth Dara": "room/images/Dara.jpg"
    }

    if doctor_name not in doctor_images.keys():
        return False
    
    doctor_image = face_recognition.load_image_file(doctor_images[doctor_name])
    doctor_encoding = face_recognition.face_encodings(doctor_image)[0]

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        unknown_image = frame

        unknown_encodings = face_recognition.face_encodings(unknown_image)
        if len(unknown_encodings) == 0:
            continue
        else:
            unknown_encoding = unknown_encodings[0]
            results = face_recognition.compare_faces([doctor_encoding], unknown_encoding)
            if True in results:
                return True
