import cv2
import numpy as np
import pandas as pd
from datetime import datetime

df_timestamp = pd.DataFrame(columns=['Start', 'End'])
status_list = [None, None]
timestamp_list = []

video_capture = cv2.VideoCapture(0)

first_frame = None

while video_capture.isOpened():

    check, frame = video_capture.read()
    status = 0

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21,21), 0)

    if first_frame is None:
        first_frame = gray_frame
        continue


    differ_frame = cv2.absdiff(first_frame, gray_frame)
    _, threshold_frame = cv2.threshold(differ_frame, 60, 255, cv2.THRESH_BINARY)
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)

    cntr,_ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in cntr:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),3)

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1] != status_list[-2]:
        timestamp_list.append(datetime.now())

    cv2.imshow('gray', gray_frame)
    cv2.imshow('diff', differ_frame)
    cv2.imshow('thresh', threshold_frame)
    cv2.imshow('result', frame)

    if cv2.waitKey(25) & 0xFF == 27:
        break
if status ==1:
    timestamp_list.append(datetime.now())

timestamp_list.pop(0)
for i in range(0,len(timestamp_list),2):
    df_timestamp = df_timestamp.append({'Start': timestamp_list[i], 'End': timestamp_list[i+1]}, 
    ignore_index=True)

df_timestamp.to_csv('Timestamp.csv')

print(df_timestamp)
video_capture.release()
cv2.destroyAllWindows()
