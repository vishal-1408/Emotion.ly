import cv2
import sys
from fer import FER
import face_recognition
import pandas as pd
import os

def emotion(impath):
    try:
        print(impath)
        image = cv2.imread(impath)
        detector=FER()
        images = detector.detect_emotions(image)
        if len(images)==0 or images==None:
            return None
        emot=(str(detector.top_emotion(image)[0]))
        return emot
    except IndexError:
        return None