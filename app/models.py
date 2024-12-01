from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return str(uuid4())

class UserModel:
    def __init__(self, user_name, user_email, mobile_number, password):
        self.user_id = generate_uuid()
        self.user_name = user_name
        self.user_email = user_email
        self.mobile_number = mobile_number
        self.password = password
        self.created_on = datetime.utcnow()
        self.last_update = datetime.utcnow()

class NoteModel:
    def __init__(self, user_id, note_title, note_content):
        self.note_id = generate_uuid()
        self.user_id = user_id
        self.note_title = note_title
        self.note_content = note_content
        self.created_on = datetime.utcnow()
        self.last_update = datetime.utcnow()
