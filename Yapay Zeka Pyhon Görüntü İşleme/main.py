import cv2
import sys
from opcua import Client, ua
import time
import matplotlib

matplotlib.use('TKAgg')

def read_input_value(node_id):
    client_node = client.get_node(node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_value_int(node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_value_bool(node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))

# OPC UA Server endpoint
url = "opc.tcp://192.168.0.1:4840"

# create cient and connect to serber
try:
    client = Client(url)
    client.connect()
    print("Connected to OPC UA Server")
except Exception as err:
    print("server not found")
    sys.exit(1)



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
    print(hue)
    color = "Undefined"
    if 1 < hue < 10:
        color = "RED"
        write_value_bool('ns=4;i=5', True)
        write_value_bool('ns=4;i=5', False)
    elif 30 < hue < 40:
        color = "GREEN"
        write_value_bool('ns=4;i=7', True)
        write_value_bool('ns=4;i=7', False)
    elif 100 < hue < 120:
        color = "BLUE"
        write_value_bool('ns=4;i=6', True)
        write_value_bool('ns=4;i=6', False)
       
    cv2.putText(frame, color, (10, 60), 0, 3, (0, 0, 0), 1)
    cv2.circle(frame, (x, y), 2, (0, 0, 0), 2)
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break