import os
import cv2
from ultralytics import YOLO
from .base import DetectionMethod
from .results import DetectionResult


class YoloModel(DetectionMethod):
    
    def __init__(self,) -> None:
        self.model = self._get_model()
        self.encoder = self.get_encoder()
        self.score_roi_min = 0.67   # минимальная уверенность модели в прогнозе
        self.max_images_select = 2  # ограничение на максимальное количество найденных рамок

    def get_encoder(self) -> dict:
        """Получение encoder для модели детекции

        Returns:
            dict: Словарь с метками, которые может прогнозировать модель (key - код прогноза модели, value - RetinaImageCropTypeOCT.name) 
        """
        return {
            0: 'retina_horizontal',
            1: 'retina_vertical',
        }

    def _get_model(self):
        """Загрузка модели
        """
        WEIGHTS_PATH = os.path.join(os.getcwd(),'retinadeepai', 'vision', 'detection', 'models', 'yolo', 'best.pt') #'detection'
        model = YOLO(WEIGHTS_PATH)
        return model

    def _predict(self, image) -> list[DetectionResult]:
        results = self.model.predict(image)
        results = results[0]
        area_crops = []
        for box in results.boxes:
            crop_type = box.cls.cpu().numpy()[0]
            _coords = box.xyxy.cpu().numpy()[0]
            coords = [_coords[0], _coords[1], _coords[0], _coords[2], _coords[2], _coords[3], _coords[0], _coords[3]]
            conf = box.conf.cpu().numpy()[0]
            if conf > self.score_roi_min:
                crop_area = DetectionResult(coords, crop_type=self.encoder[crop_type], crop_score=conf, is_obb=False)
                area_crops.append(crop_area)
        return area_crops
    
    def compute_prediction(self, image) -> list[DetectionResult]:
        crops = self._predict(image)
        return crops
    

class YoloOBBModel(DetectionMethod):
    
    def __init__(self,) -> None:
        self.model = self._get_model()
        self.encoder = self.get_encoder()
        self.score_roi_min = 0.67   # минимальная уверенность модели в прогнозе
        self.max_images_select = 2  # ограничение на максимальное количество найденных рамок

    def get_encoder(self) -> dict:
        """Получение encoder для модели детекции

        Returns:
            dict: Словарь с метками, которые может прогнозировать модель (key - код прогноза модели, value - RetinaImageCropTypeOCT.name) 
        """
        return {
            0: 'retina_horizontal',
            1: 'retina_vertical',
        }

    def _get_model(self):
        """Загрузка модели
        """
        WEIGHTS_PATH = os.path.join(os.getcwd(),'retinadeepai', 'vision', 'detection', 'models', 'yolo_obb', 'best.pt')
        model = YOLO(WEIGHTS_PATH)
        return model

    def _predict(self, image) -> list[DetectionResult]:
        results = self.model.predict(image)
        results = results[0]
        area_crops = []
        for box in results.obb:
            crop_type = box.cls.cpu().numpy()[0]
            _coords = box.xyxyxyxy.cpu().numpy()[0].flatten()
            coords = _coords
            conf = box.conf.cpu().numpy()[0]
            if conf > self.score_roi_min:
                crop_area = DetectionResult(coords, crop_type=self.encoder[crop_type], crop_score=conf, is_obb=True)
                area_crops.append(crop_area)
        return area_crops
    
    def compute_prediction(self, image) -> list[DetectionResult]:
        crops = self._predict(image)
        return crops