from ultralytics import YOLO

if __name__ == '__main__':
    # 初始训练
    model = YOLO("yolo11.yaml")# 加载预训练模型，如果本地没有会自动下载
    results = model.train(data="data.yaml", epochs=200, imgsz=1280, batch=16,project='model', name='tennis')
