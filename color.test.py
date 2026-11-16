import cv2 
import preview
import numpy as np
p = preview.Preview().start()

def see(l:list,u:list,frame) :
    lb = np.array(l)
    ub = np.array(u)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lb,ub)
    end = cv2.bitwise_and(frame,frame,mask=mask)

    kernel = np.ones((5, 5), np.uint8)
    mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours :
        return None

    target = max(contours, key=cv2.contourArea)

    (cx, cy), radius = cv2.minEnclosingCircle(target)
    cx, cy = int(cx), int(cy)

    return cx , cy

cap = cv2.VideoCapture(10,cv2.CAP_V4L2)


look = [
    ("red",   [0,   120, 70],  [10,  255, 255]),
    ("green", [40,   70,  70], [85,  255, 255]),
    ("light_blue", [85, 80, 100], [105, 255, 255]),
    ("dark_blue",  [105, 100, 40], [130, 255, 255]),]


while True :
    ret,frame = cap.read()

    if not ret :
        break

    for i in look :
        get = see(i[1],i[2],frame) 
        if get == None :
            continue
        color = i[0]
        x , y = get[0] , get[1]
        cv2.putText(frame, f"{color}", (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255, 0), 1, cv2.LINE_AA)
 
    p.push(frame)


cap.release()
cv2.destroyAllWindows()
