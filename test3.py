import cv2
import preview
p = preview.Preview().start()


def open_camera(dev='/dev/video10', w=640, h=480):
    cap = cv2.VideoCapture(dev, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)                            
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)                           
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)                            
    return cap

cap = open_camera(w=1280, h=720)

fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f'{fps} {w} {h}')

while True :
    ret,frame = cap.read()
    if not ret :
        break

    p.push(frame)

cap.release()
cv2.destroyAllWindows()
