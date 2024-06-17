def serializor(patient) -> dict:
    return {
        "id": str(patient['_id']),
        "firstName": str(patient['firstName']),
        "lastName": str(patient['lastName']),
        "email": patient['email'],
        'userType': patient['userType'],
        "verify": bool(patient.get('verify', False)),
        "dateOfBirth": str(patient.get('dateOfBirth')),
        "password": str(patient.get('password')),
        "otp": int(patient.get('otp')),
        "gender": str(patient.get('gender'))
    }


def list_serializor(patients):
    return [serializor(patient) for patient in patients]
