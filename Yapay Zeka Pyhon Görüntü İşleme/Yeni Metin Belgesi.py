import cv2
import snap7
from snap7.util import*
from snap7.types import*
def WriteMemory(plc, byte, bit, datatype, value):
    result = plc.read_area(areas['MK'],0,byte,datatype)
    if datatype==S7WLBit:
        set_bool(result,0,bit,value)
    elif datatype==S7WLByte or datatype==S7WLWord:
        set_int(result,0,value)
    elif datatype==S7WLReal:
        set_real(result,0,value)
    elif datatype==S7WLDWord:
        set_dword(result,0,value)
    plc.write_area(areas['MK'],0,byte,result)

IP = '192.168.0.1'
RACK = 0
SLOT = 1

plc = snap7.client.Client()
plc.connect(IP,RACK,SLOT)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    height, width, _ = frame.shape

    x = int(width / 2)
    y = int(height / 2)

    # Pick pixel value
    center = hsv[y, x]
    hue = center[0]

    color = "Undefined"
    if hue < 5:
        color = "RED"
        WriteMemory(plc, 0, 7, S7WLByte, 1)
        time.sleep(1)
    elif 40 < hue < 78:
        color = "GREEN"
        WriteMemory(plc, 0, 6, S7WLByte, 1)
        time.sleep(1)
    elif 100 < hue < 131:
        color = "BLUE"
        WriteMemory(plc, 0, 5, S7WLByte, 1)
        time.sleep(1)

    cv2.putText(frame, color, (10, 60), 0, 3, (0, 0, 0), 3)
    cv2.circle(frame, (x, y), 2, (0, 0, 0), 2)
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break