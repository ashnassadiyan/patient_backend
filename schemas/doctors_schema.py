def serializor(doctor) -> dict:
    return {
        "id": str(doctor['_id']),
        "firstName": str(doctor['firstName']),
        "lastName": str(doctor['lastName']),
        "email": doctor['email'],
        'specialized': doctor['specialized'],
    }


def list_serializor(doctors):
    return [serializor(doctor) for doctor in doctors]
