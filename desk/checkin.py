
# checks in a patient
def checkin_patient(patient_id):
    # check if patient is already checked in
    if check_is_patient_checked_in(patient_id):
        return "already checked in"

    # get patient basic information
    patient_basic_information = get_patient_basic_information(patient_id)

    # add patient to doctor queue
    preferred_doctor = patient_basic_information["preferred doctor"]
    add_patient_to_doctor_queue(patient_id, preferred_doctor)
    
    return

# checks if a patient is checked in
def check_is_patient_checked_in(patient_id):
    # retrieves checked in list from firebase
    # see if patient in list, return True if yes, False if no
    return

# retrieves patient basic information from firebase
def get_patient_basic_information(patient_id):
    # retrieves from firebase
    
    response = {}
    response["name"] = "Jack"
    response["appointment history"] = ["12312", "123123", "1211"]
    response["preferred doctor"] = "Sumanth Dara"
    return response

# adds a patient id to the preferred doctor's queue
def add_patient_to_doctor_queue(patient_id, preferred_doctor):
    # adds to firebase
    return