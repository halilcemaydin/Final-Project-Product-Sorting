import Config
from ProductDetector import *
from PLCUtils import *

def main():
    camera_source = Config.CAMERA_SOURCE
    model_path = Config.MODEL_PATH
    device = Config.DEVICE
    input_shape = (Config.INPUT_SHAPE, Config.INPUT_SHAPE)
    plc_url = Config.PLC_URL

    video_cap = cv2.VideoCapture(camera_source)

    if not video_cap.isOpened():
        print('Unable to open camera from source :', camera_source)
        return
    
    client = client_connection(url=plc_url)
    if client == None:
        #return
        pass

    detector = ProductDetector(model_name=model_path, device=device, conf_th=0.90)
    
    while True:
        ret, frame = video_cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, input_shape)

        #Detection
        start_time = time()
        results = detector.predict(frame)
        end_time = time()

        #Visualization
        fps = 1 / (end_time - start_time)
        obj_class, frame = detector.plot_boxes(results, frame)
        cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2) # print(f"her saniye frame yaz : {fps}")
        cv2.imshow("YOLOv5 Detection", frame)
        
        #Degisecek, Calismayabilir
        """
        if obj_class == "Red":
            write_value_bool(client, 'ns=4;i=2', True)
            write_value_bool(client, 'ns=4;i=2', False)

        if obj_class == "Green":
            write_value_bool(client, 'ns=4;i=4', True)
            write_value_bool(client, 'ns=4;i=4', False)

        if obj_class == "Blue":
            write_value_bool(client, 'ns=4;i=3', True)
            write_value_bool(client, 'ns=4;i=3', False)

        else:
            continue
        """
        if cv2.waitKey(1) == 27:
            break

    video_cap.release()
    cv2.destroyAllWindows()

    if device == "cuda":
        detector.clear_gpu_cache()
        
if __name__ == "__main__":
    main()