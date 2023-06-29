import snap7
import cv2
plc = snap7.client.Client()
plc.connect('192.168.0.1 ', 0, 1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)                                  #   E   D   E   M


    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]
    if hue_value < 5: #KIRMIZI KONTAK
        db_number = 1
        start_offset = 0
        bit_offset = 0
        value = 1
    elif 33< hue_value < 75: #YEŞİL KONTAK
        db_number = 1
        start_offset = 0
        bit_offset = 1
        value = 1
    elif 100< hue_value < 130: #MAVİ KONTAK
        db_number = 1
        start_offset = 0
        bit_offset = 2
        value = 1
    else:
        db_number = 1
        start_offset = 0
        bit_offset = 0
        value = 0
                                                                  #   E   D   E   M

    def WriteBool(db_number, start_offset, bit_offset, value):
        reading = plc.db_read(db_number, start_offset, 1)
        snap7.util.set_bool(reading, 0, bit_offset, value)
        plc.db_write(db_number, start_offset, reading)
        return None



    def ReadBool(db_number, start_offset, bit_offset):
        reading = plc.db_read(db_number, start_offset, 1)
        a = snap7.util.get_bool(reading, 0, bit_offset)
        print('DB Number: ' + str(db_number) + 'Bit: ' + str(start_offset) + '.' + str(bit_offset) + 'Value: ' + str(a))


    WriteBool(db_number, start_offset, bit_offset, value)

    ReadBool(db_number, start_offset, bit_offset)

    pixel_center_bgr = frame[cy, cx]
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
                                                                           #   E   D   E   M

