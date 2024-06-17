def serializor(availability) -> dict:
    return {
        "id": str(availability['_id']),
        "available": str(availability['available']),
        "doctor_id": str(availability['doctor_id'])
    }


def list_serializor(availabilities):
    return [serializor(availability) for availability in availabilities]


# {
#  '_id': ObjectId('666edf323034450a135bff59'),
#  'available': datetime.datetime(2024, 6, 20, 0, 0),
#  'doctor_id': ObjectId('666568009c0cc47c0536b69a'),
#  'doctor_info': {
#      '_id': ObjectId('666568009c0cc47c0536b69a'),
#      'firstName': 'Nawangi',
#      'lastName': 'Sadiyan',
#      'email': 'ashnassadiyan@gmail.com',
#      'specialized': 'family doctor'
#  }}