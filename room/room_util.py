import face_recognition
import cv2
import time
import pyrebase
import firebase_config


firebase_config = firebase_config.set_firebase_config()
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
token = auth.create_custom_token("room")
user = auth.sign_in_with_custom_token(token)
db = firebase.database()

doctor_name = "NO DOCTOR"
patient_name = "NO PATIENT"

room_number = "NO ROOM NUMBER"

# reads the "room" file to get the room number
def get_room_number():
    global room_number
    with open("room/room", "r") as room_number_file:
        room_number = room_number_file.readline()
    return room_number


# gets the room information from firebase
def get_room_information(room_number):
    # retrieves from firebase
    room_information = db.child("rooms").child("rooms").child(room_number)
    if str(type(room_information)) == "<class 'NoneType'>":
        return "free"

    if room_information.child("doctor").get().val() == "":
        return "free"
    print(room_information.get().val())
    doctor_name = room_information.child("doctor").get().val()
    patient_id = room_information.child("patient").get().val()
    return doctor_name, patient_id


# get patient medical data from firebase
def get_patient_medical(patient_id):
    # retrieves from firebase
    patient_medical_information = db.child("patient information").child(patient_id)
    if str(type(patient_medical_information)) == "<class 'NoneType'>":
        return "invalid id"
    return patient_medical_information


def periodicLoop():
    while True:
        doctor, patient_id = get_room_information(room_number)
        print(str(doctor))
        if doctor == "" or doctor == "NO DOCTOR" or doctor == None:
            time.sleep(5)
            continue
        break
    return


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
