import os
from ultralytics import YOLO
from django.conf import settings

# YOLO 모델을 전역 변수로 로드
model_path = os.path.join(settings.MEDIA_ROOT, 'models', 'YOLOv8n-cls_Rice_Disease.pt')
model = YOLO(model_path)


def detect_disease(image_path):
    result = model(image_path)

    for r in result:
        probs = list(r.probs.data)
        classes = r.names

        highest_prob = max(probs)
        highest_prob_index = probs.index(highest_prob)

        return classes[highest_prob_index], highest_prob * 100
