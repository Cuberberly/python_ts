import cv2
import numpy as np


detector = cv2.QRCodeDetector()
detector2 = cv2.wechat_qrcode_WeChatQRCode(
    "/home/lckfb/py_work/models/detect.prototxt",
    "/home/lckfb/py_work/models/detect.caffemodel",
    "/home/lckfb/py_work/models/sr.prototxt",
    "/home/lckfb/py_work/models/sr.caffemodel")


#打开720p：w=1280，h=720
def open_camera(dev='/dev/video10', w=640, h=480):
    cap = cv2.VideoCapture(dev, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)                            
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)                           
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)                            
    return cap


#需要传入720p图像，返回扫描结果,没扫到return None
def wc_scanner(frame) :

    frame = frame[180:540,320:960]
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)

    clahe= cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    frame = clahe.apply(frame)

    blur = cv2.GaussianBlur(frame, (0, 0), 2.0)
    frame = cv2.addWeighted(frame, 1.5, blur, -0.5, 0)

    data, points = detector2.detectAndDecode(frame)

    if data :
        return data
    else :
        return None

#找轮廓的，后面函数用得到
def find_contour (frame,high:list,low:list) :
    lb = np.array(low)
    ub = np.array(high)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lb,ub)

    kernel = np.ones((5, 5), np.uint8)
    mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours :
        return None

    target = max(contours, key=cv2.contourArea)

    return target


#high和low数据顺序是[h,s,v],return物品中心在画面的水平位置，这个是看球的
def hsv_color_circle (frame,high:list,low:list) :
    target = find_contour(frame,high,low)

    # 面积筛，之后测试在完善
    # s = cv2.contourArea(target)
    # if s < xx :
    #     return None

    if target is not None:
        (cx, cy), radius = cv2.minEnclosingCircle(target)
        cx, cy = int(cx), int(cy)
        return cx,cy
    else :
        return None


#同上，这个是看圆台的，不过这个是矩形识别，x准y不准
def hsv_color_square (frame,high:list,low:list) :
    target = find_contour(frame,high,low)

    # 面积筛，之后测试在完善
    # s = cv2.contourArea(target)
    # if s < xx :
    #     return None

    if target is not None :
        x, y, w, h = cv2.boundingRect(target)
        cx = (x + w )/ 2
        cy = (y + h )/ 2
        return cx
    else :
        return None

