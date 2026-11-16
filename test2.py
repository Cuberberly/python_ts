import serial
import time

ser = serial.Serial(port='dev/ttyS3',baudrate = 115200)

if __name__ == "__main__" :
    while True :
        ser.write("test".encode("utf_8"))
        time.sleep(1)