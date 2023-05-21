import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
# import subprocess
import mysql.connector


model=YOLO('yolov8s.pt')


area1=[(560,274),(712,375),(673,389),(530,289)]

area2=[(480,280),(648,396),(609,408),(430,290)]
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :
        colorsBGR = [x, y]
        print(colorsBGR)


cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('VID20230520030843.mp4')


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count=0

tracker = Tracker()
people_entering = {}
entering = set()
people_exiting = {}
exiting = set()
while True:
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 2 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))

    results=model.predict(frame)

    a=results[0].boxes.boxes
    px=pd.DataFrame(a).astype("float")

    list=[]

    for index,row in px.iterrows():


        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'person' in c:
            list.append([x1,y1,x2,y2])
    bbox_id = tracker.update(list)
    for bbox in bbox_id :
        x3,y3,x4,y4,id = bbox
        result = cv2.pointPolygonTest(np.array(area2, np.int32), ((x4, y4)), False)
        if result >= 0:
            people_entering[id] = (x4,y4)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0,0,255), 2)
        if id in people_entering :
            result1 = cv2.pointPolygonTest(np.array(area1, np.int32), ((x4, y4)), False)
            if result1 >= 0:
                cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                cv2.circle(frame,(x4,y4),4,(255,0,255),-1)
                cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,(0.5),(255,255,255),1)
                entering.add(id)

        result2 = cv2.pointPolygonTest(np.array(area1, np.int32), ((x4, y4)), False)
        if result2 >= 0:
            people_exiting[id] = (x4, y4)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0,255,0), 2)
        if id in people_exiting:
            result3 = cv2.pointPolygonTest(np.array(area2, np.int32), ((x4, y4)), False)
            if result3 >= 0:
                cv2.rectangle(frame, (x3, y3), (x4, y4), (255,0, 255), 2)
                cv2.circle(frame, (x4, y4), 4, (255, 0, 255), -1)
                cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, (0.5), (255, 255, 255), 1)
                exiting.add(id)


    cv2.polylines(frame,[np.array(area1,np.int32)],True,(255,0,0),2)
    cv2.putText(frame,str('1'),(644,281),cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    cv2.polylines(frame,[np.array(area2,np.int32)],True,(255,0,0),2)
    cv2.putText(frame,str('2'),(528,337),cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    print(len(entering))
    print(len(exiting))
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="counter_db"
    )

    cursor = conn.cursor()

    live_data = [(len(entering), len(exiting))]

    for data in live_data:
        query = "INSERT INTO `counter_db`.`in_out` (`in_in`, `out_out`) VALUES (%s, %s )"
        cursor.execute(query, data)

    conn.commit()

    cursor.close()
    conn.close()



cap.release()
cv2.destroyAllWindows()



































