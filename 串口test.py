import serial
import time

ser = serial.Serial(port='dev/ttyS3',baudrate = 115200,timeout= 0.1)

while True :
    ser.write("test".encode("utf_8"))
    time.sleep(0.5)

    for i in range(5) :
        line = ser.readline()     
        if not line:
            continue                    
        text = line.decode("ascii", "replace")
        if not text:
            continue
        print(f'{text}')
        break





if __name__ == "__main__" :
    while True :
        ser.write("test".encode("utf_8"))
        time.sleep(1)

    while True:
        line = ser.readline()     
        if not line:
            continue                    
        text = line.decode("ascii", "replace").strip()
        if not text:
            continue
        print("收到:", text)

