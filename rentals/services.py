import datetime
from uuid import UUID


def dateTransform(data):
    temp = datetime.datetime.strftime(data, "%Y-%m-%d")
    return datetime.datetime.strptime(temp, "%Y-%m-%d").date()


def verify_uuid(uuid):
    try:
        uuid_obj = UUID(uuid, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid
