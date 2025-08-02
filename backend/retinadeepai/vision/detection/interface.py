from retinadeepai.models import (
    RetinaDetectionTask,
    RetinaFileUpload,
    RetinaImageCropOCT,
    RetinaImageCropTypeOCT,
)
from retinadeepai.serializers import RetinaImageCropOCTSerializer
from retinadeepai.vision.classification.yolo import YoloOrientation
from .base import DetectionMethod
from .results import DetectionResult
from PIL import Image, ImageDraw, ImageTransform
from io import BytesIO
import cv2
import numpy as np
from django.core.files.base import ContentFile


class RetinaMapDetectionInterface:
    """Обертка для решения задачи детекции"""

    def __init__(self, task_guid: str, net: DetectionMethod) -> None:
        self.task_guid = task_guid
        self.crops = []
        self.net = net

    def solve(self):
        try:
            task_detection = RetinaDetectionTask.objects.get(guid=self.task_guid)
            task_detection.status = task_detection.TaskStatus.PROCESSED
            task_detection.save()
            image = cv2.imread(task_detection.image.image.path)
            area_crops = self.net.compute_prediction(image)
            crops = self._save_crops(task_detection, area_crops)
            task_model = self._save_cover(task_detection, area_crops)
            task_detection.status = task_detection.TaskStatus.SUCCESS
            task_detection.save()
            return task_model, crops
        except Exception as e:
            task_detection.status = task_detection.TaskStatus.ERROR
            raise e

    def _save_crops(
        self, task_detection: RetinaDetectionTask, area_crops: list[DetectionResult]
    ) -> list[RetinaImageCropOCT]:
        """Сохранение найденных фрагментов на изображении в базу"""
        crops = []

        if len(area_crops) > 0:
            for ind, area_crop in enumerate(area_crops):
                retina_crop_type = RetinaImageCropTypeOCT.objects.get(
                    name=area_crop.crop_type
                )
                crop = RetinaImageCropOCT(
                    type_oct_id=retina_crop_type.id,
                    task_detection=task_detection,
                    confidence=area_crop.crop_score,
                )
                crop.save()
                # Тут разворачиваем изображение если это obb task
                if area_crop.is_obb:
                    research_file_jpg = Image.open(task_detection.image.image.path)
                    coords_points = area_crop.get_by_points()
                    coords_list = area_crop.points
                    rect = cv2.minAreaRect(np.array(coords_points))
                    sizes = rect[1]
                    x = int(sizes[0])
                    y = int(sizes[1])
                    # По определению ширина должна быть больше чем высота
                    if y > x:
                        x, y = y, x
                    retina_map_crop = research_file_jpg.transform((x,y), ImageTransform.QuadTransform(coords_list))
                    orientation_model = YoloOrientation()
                    retina_map_crop = orientation_model.make_rotate_predict(retina_map_crop)
                else:
                    research_file_jpg = Image.open(task_detection.image.image.path)
                    retina_map_crop = research_file_jpg.crop(
                        (
                            area_crop.points[0],
                            area_crop.points[1],
                            area_crop.points[4],
                            area_crop.points[5],
                        )
                    )
                retina_map_crop_io = BytesIO()
                retina_map_crop.save(retina_map_crop_io, format="JPEG")
                crop.image.save(
                    f"retina_map_{ind}.jpg",
                    ContentFile(retina_map_crop_io.getvalue()),
                )
                crop.save()
                crops.append(crop)
        return crops

    def _save_cover(
        self,
        task_detection: RetinaDetectionTask,
        area_crops: list[DetectionResult],
        width=5,
        color="#38cd24",
    ):
        if len(area_crops) > 0:
            with Image.open(task_detection.image.image.path) as img:
                draw = ImageDraw.Draw(img)
                for crop_area in area_crops:
                    if crop_area.is_obb:
                        draw.line(
                            [*crop_area.get_top_left(), *crop_area.get_top_right()],
                            fill=color,
                            width=width,
                        )
                        draw.line(
                            [*crop_area.get_top_right(), *crop_area.get_bottom_right()],
                            fill=color,
                            width=width,
                        )
                        draw.line(
                            [*crop_area.get_bottom_right(),*crop_area.get_bottom_left(),],
                            fill=color,
                            width=width,
                        )
                        draw.line(
                            [*crop_area.get_bottom_left(), *crop_area.get_top_left()],
                            fill=color,
                            width=width,
                        )
                    else:
                        draw.rectangle(crop_area.get_xyxy(), width=width, outline=color)
                retina_map_crop_io = BytesIO()
                img.save(retina_map_crop_io, format="JPEG")
                task_detection.detection_cover.save(
                    "detection.jpg", ContentFile(retina_map_crop_io.getvalue())
                )
            task_detection.save()
            return task_detection
