import cv2
import preview
from pyzbar.pyzbar import decode
p = preview.Preview().start()
detector = cv2.QRCodeDetector()
detector2 = cv2.wechat_qrcode_WeChatQRCode(
    "/home/lckfb/py_work/models/detect.prototxt",
    "/home/lckfb/py_work/models/detect.caffemodel",
    "/home/lckfb/py_work/models/sr.prototxt",
    "/home/lckfb/py_work/models/sr.caffemodel")

def open_camera(dev='/dev/video10', w=640, h=480):
    cap = cv2.VideoCapture(dev, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)                            
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)                           
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    print('1')                            
    return cap

cap = open_camera(w=1280, h=720)
# cap = cv2.VideoCapture(10,cv2.CAP_V4L2)

fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f'{fps} {w} {h}')

last_data = ""
while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = frame[180:540,320:960]
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    # frame = cv2.pyrUp(frame)


    clahe= cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    frame = clahe.apply(frame)

    blur = cv2.GaussianBlur(frame, (0, 0), 2.0)
    frame = cv2.addWeighted(frame, 1.5, blur, -0.5, 0)


    # data = decode(frame)

    data, points = detector2.detectAndDecode(frame)


    if data:
        last_data = data

        cv2.putText(frame, f"QR: {data}", (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        print(data)

    p.push(frame)

cap.release()
cv2.destroyAllWindows()
