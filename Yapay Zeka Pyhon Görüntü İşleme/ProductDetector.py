import torch
import numpy as np
import cv2
import sys
from opcua import Client, ua
from time import time
import Config
import gc


class ProductDetector: 
    
    def __init__(self, model_name, device, conf_th = 0.8): 

        self.model = self.load_model(model_name)
        self.device = device
        self.model.to(self.device)
        self.model.eval()
        self.classes = self.model.names
        self.conf_th = conf_th
        print("Using Device: ", self.device)

    @staticmethod
    def load_model(model_name=None): # Pytorch hub'dan Yolov5 modelini indiriyoruz ve bunu modüle geri döndürüyoruz.
        
        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    def predict(self, frame): # Kameradan aldığı görüntüyü modele sokarak ondan tahmin oranı alıyoruz.
        frame = [frame]
        with torch.no_grad():
            results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x): # Classlarımızı labela dönüştürüyoruz.
        return self.classes[int(x)]
    
    def plot_boxes(self, results, frame): # Aranan objenin hangi konumlar içinde olduğunu buluyoruz.
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        obj_class = ""
        for i in range(n):
            row = cord[i]
            if row[4] >= self.conf_th: # Hangi doğruluk değerinin üstünü ekrana yazdırmak istiyorsak yazıyoruz.
                obj_class = self.class_to_label(labels[i])
                if obj_class == "Mavi":
                    obj_class = "Red"
                elif obj_class == "Red":
                    obj_class = "Blue"
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, obj_class, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return obj_class, frame


    def clear_gpu_cache(self):
        print('Clearing gpu cache ...')
        self.model = None
        gc.collect()
        with torch.no_grad():
            torch.cuda.empty_cache()