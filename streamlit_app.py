import cv2
import numpy as np
import strealit as st

st.title('Sinais')

camera = cv2.VideoCapture("http://177.72.3.203:8001/")

while(True):
    ret, frame = camera.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
