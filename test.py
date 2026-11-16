import cv2
import preview
p = preview.Preview().start()

cap = cv2.VideoCapture(10,cv2.CAP_V4L2)
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