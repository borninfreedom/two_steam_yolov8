# 测试
from ultralytics import YOLO 
model = YOLO('/root/autodl-tmp/projects2025/TwoStream_Yolov8-main/runs/detect/train11/weights/best.pt') 
metrics = model.val(data='/root/autodl-tmp/projects2025/TwoStream_Yolov8-main/data/fire_detect_rgb_ir.yaml',split='test',imgsz=640,batch=16,conf=0.8)
