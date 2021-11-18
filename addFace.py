import face_recognition
import json

def main():
    file = '1.jpg'
    DATABASE_FILE = 'db.json'
    LAST_PERSON_ID = 0

    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as read_file:
            persons = json.load(read_file)
    except:
        persons = []

    for person in persons:
        if person['id'] >= LAST_PERSON_ID:
            LAST_PERSON_ID = person['id'] + 1

    name_ru = input('ru -> ')
    name_en = input('en -> ')

    face_encodings = face_recognition.face_encodings(face_recognition.load_image_file(file))[0].tolist()

    new_person = {
        'id': LAST_PERSON_ID,
        'ru': name_ru,
        'en': name_en,
        'face_encoding': face_encodings,
    }

    persons.append(new_person)
    with open(DATABASE_FILE, 'w', encoding = 'utf-8') as jsonfile:
        json.dump(persons, jsonfile, ensure_ascii = False)

if __name__ == '__main__':
    main()
