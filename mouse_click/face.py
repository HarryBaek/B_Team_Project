from keras.models import load_model
from PIL import Image, ImageOps
import cv2
import numpy as np
import test1
import time
import datetime
import pygame

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

access = ''

path = ''
path1 = 'permission_people/'

all_bye = False

while True:
    ret, frame_f = cap.read()
    if not ret: break
    frame_f = cv2.flip(frame_f,1)
    frame = frame_f.copy()

    size = (224, 224)
    image = cv2.resize(frame, size)
    image = Image.fromarray(image)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

    image = np.array(image)

    max_prediction = max(prediction[0])
    print(prediction[0][0:3])

    if access == True:
        cv2.putText(frame_f,'login acess',(600,600),
                cv2.FONT_HERSHEY_PLAIN,5,(0,255,0),5)

        datetime_object = datetime.datetime.now()
        date_time = datetime_object.strftime("%m_%d_%Y__%H_hor_%M_min_%S_sec")

        cv2.imwrite(path1+f'_{date_time}.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

        all_bye = test1.hand_ocr(cap,cap2)
        pygame.init()
        pygame.mixer.init()
        sound4 = pygame.mixer.Sound(path+"close.wav" )
        sound4.play()

    elif access == False:
        cv2.putText(frame_f,'who are you?',(600,600),
                cv2.FONT_HERSHEY_PLAIN,5,(0,0,255),5)

    if prediction[0][1] > 0.4:
        access = True

    elif prediction[0][2] > 0.4:
        access = True   

    else :
        access = False
    
    if access == True:
        cv2.putText(frame_f,'login access',(600,400),
                cv2.FONT_HERSHEY_PLAIN,5,(0,255,0),5)
        time.sleep(0.1)

    cv2.imshow('img', frame_f)
    # cv2.imshow('img2', image)

    if cv2.waitKey(1) == 27: break
    if all_bye == True : break

cv2.destroyAllWindows()
