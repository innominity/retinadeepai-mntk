from ultralytics import YOLO
import torch
import os
import cv2
import numpy as np
from PIL import Image
from .results import AnalysisResult
from .base import ClassificationMethod

from retinadeepai.vision.classification.yolo_cam.eigen_cam import EigenCAM
from retinadeepai.vision.classification.yolo_cam.utils.image import show_cam_on_image, scale_cam_image


class YoloAnalysis(ClassificationMethod):

    WEIGHTS_ROOT_PATH = os.path.join(
        os.getcwd(),
        "retinadeepai",
        "vision",
        "classification",
        "models",
        "analysis",
        "yolo",
    )

    def __init__(self, encoder, model_dir_path: str):
        self.encoder = encoder
        self.model_dir_path = os.path.join(self.WEIGHTS_ROOT_PATH, model_dir_path)

    def get_encoder(self) -> dict:
        return self.encoder

    def _get_model(self):
        # хак чтобы можно было передавать папку с моделью не парясь о названии модели
        if os.path.isdir(self.model_dir_path):
            models_list = os.listdir(self.model_dir_path)
            if len(models_list) > 0 and models_list[0].endswith(".pt"):
                # только если есть в папке модели и определенного расширения
                model_name = models_list[0]
                model_path = os.path.join(self.model_dir_path, model_name)
                model = YOLO(model_path)
                return model
            else:
                raise Exception(f"Не удалось загрузить модель {self.__repr__()}")
        else:
            raise Exception(f"Не удалось загрузить модель {self.__repr__()}")

    def predict(self, img: np.ndarray) -> list[AnalysisResult]:
        model = self._get_model()
        predict_results = model.predict(img)
        label_mark = list(self.encoder.keys())[0]
        probs = predict_results[0].probs.data.cpu().numpy()
        encoder_reverse = predict_results[0].names
        encoder = {v:k for k,v in encoder_reverse.items()}
        score = probs[encoder[label_mark]]
        result = AnalysisResult(label_mark, score)
        return [result]
    
    def _make_cam(self, image):
        model = self._get_model()
        img = cv2.resize(image, (640, 640))
        rgb_img = img.copy()
        img = np.float32(img) / 255
        target_layers = [model.model.model[-2]]
        cam = EigenCAM(model, target_layers,task='cls')
        grayscale_cam = cam(rgb_img)[0, :, :]
        img_explain = show_cam_on_image(img, grayscale_cam, use_rgb=True)
        return Image.fromarray(img_explain)


    def make_explain(self, image):
        return self._make_cam(image)


class YoloOrientation:

    def get_encoder(self):
        return {"no_rotate": 0, "rotate": 1}

    def get_model(self):
        WEIGHTS_PATH = os.path.join(
            os.getcwd(),
            "retinadeepai",
            "vision",
            "classification",
            "models",
            "orientation",
            "yolo",
            "best.pt",
        )
        model = YOLO(WEIGHTS_PATH)
        return model

    def make_rotate_predict(self, image_orig: Image) -> Image:
        model = self.get_model()
        encoder = self.get_encoder()
        probs = {}
        for angle in [0, 90, 180, 270]:
            img_rotate = image_orig.rotate(angle)
            results = model.predict(img_rotate)
            probs_iter = results[0].probs.data.cpu().numpy()
            probs[angle] = probs_iter[encoder["no_rotate"]]
        rotate_angle = max(probs, key=probs.get)
        return image_orig.rotate(rotate_angle)
