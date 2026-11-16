import cv2
import preview
from tool import hsv_color_circle,hsv_color_square 
p = preview.Preview().start()

cap = cv2.VideoCapture(10,cv2.CAP_V4L2)

look = [
    ("red",   [0,   110, 50],  [8,  255, 255]),
    ('red2',[165,110,50],[180,255,255]),
    ('black',[0,0,0],[180,90,70]),
    ("green", [40,   70,  70], [85,  255, 255]),
    ("light_blue", [85, 80, 100], [105, 255, 255]),
    ("dark_blue",  [105, 100, 40], [130, 255, 255]),]


while True :
    ret,frame = cap.read()

    if not ret :
        break

    for i in look :



        get = hsv_color_circle(frame,i[2],i[1])
        #get = hsv_color_square(frame,i[2],i[1])



        if get == None :
            continue
        color = i[0]
        x = get[0] , get[1]
        cv2.putText(frame, f"{color}", (x), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255, 0), 1, cv2.LINE_AA)
 
    p.push(frame)
