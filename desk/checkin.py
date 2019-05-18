import pyrebase
import firebase_config

firebase_config = firebase_config.set_firebase_config()

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

token = auth.create_custom_token("desk")
user = auth.sign_in_with_custom_token(token)

db = firebase.database()

# checks in a patient
def checkin_patient(patient_id):
    # check if patient is already checked in
    if check_is_patient_checked_in(patient_id):
        return "already checked in"

    # get patient basic information
    patient_basic_information = get_patient_basic_information(patient_id)
    if patient_basic_information == "invalid id":
        return "invalid id"

    # add patient to queue
    add_patient_to_queue(patient_id)

    # add patient to checked in
    add_patient_to_checked_in(patient_id)
    
    return

def add_patient_to_checked_in(patient_id):
    checked_in = db.child("rooms").child("checked in").get().val()
    if str(type(checked_in)) == "<class 'NoneType'>":
        checked_in = []
    
    checked_in.append(patient_id)
    db.child("rooms").child("checked in").set(checked_in)
    return

# checks if a patient is checked in
def check_is_patient_checked_in(patient_id):
    # retrieves checked in list from firebase
    checked_in = db.child("rooms").child("checked in").get().val()

    if str(type(checked_in)) == "<class 'NoneType'>":
        return False

    # see if patient in list, return True if yes, False if no
    if patient_id in checked_in:
        return True
    return False

# retrieves patient basic information from firebase
def get_patient_basic_information(patient_id):
    # retrieves from firebase
    patient_basic_information = db.child("patient information").child(patient_id)
    if str(type(patient_basic_information)) == "<class 'NoneType'>":
        return "invalid id"

    print(str(patient_basic_information))
    return patient_basic_information

# add patient id to general queue
def add_patient_to_queue(patient_id):
    current_queue = db.child("rooms").child("queue").get().val()
    if str(type(current_queue)) == "<class 'NoneType'>":
        current_queue = []

    current_queue.append(patient_id)
    db.child("rooms").child("queue").set(current_queue)
    return

# adds a patient id to the preferred doctor's queue
def add_patient_to_doctor_queue(doctor, patient_id, patient_room):
    # adds to firebase
    patient_list = db.child("rooms").child("doctors").child(doctor).get().val()
    patient_list.append({"id": patient_id, "room": patient_room})
    db.child("rooms").child("doctors").child(doctor).set(patient_list)
    return

# moved patients from queue to rooms, updates doctor queues
def align_rooms():
    room_list = db.child("rooms").child("rooms").get().val()
    queue = db.child("rooms").child("queue").get().val()

    if str(type(queue)) == "<class 'NoneType'>":
        return

    for room in room_list.items():
        if room[1]["doctor"] == "":
            patient_id = queue[0]
            room[1]["doctor"] = db.child("patient information").child(patient_id).child("preferred physician").get().val()
            room[1]["patient"] = patient_id
            db.child("rooms").child("rooms").child(room[0]).update(room[1])

            queue.pop(0)
            db.child("rooms").child("queue").set(queue)

            print("updated room")
    
    