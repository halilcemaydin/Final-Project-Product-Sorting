import torch

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_PATH = "./models/best.pt"
CAMERA_SOURCE = 0
INPUT_SHAPE = 640
PLC_URL = "opc.tcp://192.168.0.1:4840"