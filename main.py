import cv2
from fps import FPS
import face_recognition
import os
import numpy as np
import json
import threading
import time

INDEX = []
NAME_EN = []
NAME_RU = []
FACE = []


def main():
    # setting
    FPS_NOW = 0
    SETTING_FPS = True
    progressBar = 0
    delay = 30
    IS_greetings = []
    step = 10
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

    # setting value
    version = '0.4'

    # initialization class
    if SETTING_FPS: cameraFPS = FPS()

    # main loop
    openFileJson = getJsonData('db.json')
    while openFileJson:
        ret, photo = camera.read()
        height, width = photo.shape[:2]
        photo = cv2.flip(photo, 1)
        face_locations = face_recognition.face_locations(photo)
        face_encodings = face_recognition.face_encodings(photo, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            name = 'unidentified'
            name_ru = ''

            matches = face_recognition.compare_faces(FACE, face_encoding)
            
            if True in matches:
                first_match_index = matches.index(True)
                name = NAME_EN[first_match_index]

            face_distances = face_recognition.face_distance(FACE, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]: 
                name = NAME_EN[best_match_index]
                name_ru = NAME_RU[best_match_index]

            # True if you have a face
            if True in matches:
                cv2.rectangle(photo, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(photo, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                progressBar += step
            else:
                cv2.rectangle(photo, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(photo, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                progressBar -= step
            cv2.putText(photo, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            # END True if you have a face
            if progressBar <= -100 - step:
                greeting = threading.Thread(target=greetings, args=(name_ru, False))
                greeting.start() 

            if progressBar >= 100 + step:
                progressBar = 0
                greeting_status = {
                    'ID': INDEX[best_match_index],
                    'time_start':time.time(),
                    'IS_greeting': False,
                }
                
                # IS_greetings
                if  IS_greetings:
                    for IS_greeting in IS_greetings:
                        if (time.time() - IS_greeting['time_start']) >= delay:
                            IS_greeting['time_start'] = time.time()
                            greeting = threading.Thread(target=greetings, args=(name_ru,))
                            greeting.start()                    
                if not IS_greetings: 
                    IS_greetings.append(greeting_status)
                    greeting = threading.Thread(target=greetings, args=(name_ru,))
                    greeting.start() 
                else:                    
                    for IS_greeting in IS_greetings:
                        if IS_greeting['ID'] == greeting_status['ID']:
                            break
                    if greeting_status['IS_greeting']:
                        IS_greetings.append(greeting_status)
                        greeting = threading.Thread(target=greetings, args=(name_ru,))
                        greeting.start() 
            if progressBar <= -100 - step: progressBar = 0
            # END IS_greetings

        # FPS
        if SETTING_FPS:
            cameraFPS_OR_None = cameraFPS.counter()
            if cameraFPS_OR_None != None: FPS_NOW = cameraFPS_OR_None
        # END FPS

        # informationOutput
        informationOutputSetting = {
            'setting': {
                'height': height,
                'width': width,
                'position': 'top-left',
                'padding': 20,
            },
            'text': [
                f'version: {version}',
            ]
        }
        
        if SETTING_FPS: informationOutputSetting['text'].append(f'FPS: {FPS_NOW}')
        informationOutput(informationOutputSetting, photo)
        # END informationOutput

        # Face-recognition
        cv2.imshow('Face-recognition', photo)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Face-recognition

    camera.release()
    cv2.destroyAllWindows()

# greetings
def greetings(name, FLAG = True):
    if FLAG:
        os.system('echo "Здравствуйте ' + str(name) + '" | festival --tts --language russian')
    else:
        os.system('echo "Здравствуйте не опознаный обект" | festival --tts --language russian')

# END greetings

# getPictures
def getPictures(directory):
    check = False
    files = os.listdir(directory)
    for img in files:
        (name, _) = img.split('.')
        face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(directory + img))[0]
        FACE.append(face_encoding)
        NAME_EN.append(name)
        check = True
    return check
# END getPictures

# getJsonData
def getJsonData(DATABASE_FILE):
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as read_file:
            persons = json.load(read_file)
    except:
        persons = []
        return False

    for person in persons:
        INDEX.append(person['id'])
        NAME_EN.append(person['en'])
        NAME_RU.append(person['ru'])
        FACE.append(person['face_encoding'])
    return True
# END getJsonData

# informationOutput
def informationOutput(informationOutputSetting, photo):
    padding = informationOutputSetting['setting']['padding']
    # top-left
    if informationOutputSetting['setting']['position'] == 'top-left':
        width = 0
        for text in informationOutputSetting['text']:
            cv2.putText(photo, str(text), (0 + padding, 0 + padding + width), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2)
            width = width + padding
    # top-right
    
if __name__ == '__main__':
    main()
