import cv2


img = None       
for i in range(12) :
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2) 
    ret, frame = cap.read() 
    cap.release()
    # print(f'{i}')                        
    if ret and frame is not None:
        print(f'camera index: {i}')
        break
print('end')