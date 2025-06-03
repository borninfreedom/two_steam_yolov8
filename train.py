#训练
from ultralytics import YOLO
import ultralytics.nn.tasks
model = YOLO('/root/autodl-tmp/projects2025/TwoStream_Yolov8-main/yaml/PC2f_MPF_yolov8n.yaml')
print(f'{model = }')
results = model.train(data='/root/autodl-tmp/projects2025/TwoStream_Yolov8-main/data/fire_detect_rgb_ir.yaml',batch=16,epochs=400)
