from retinadeepai.models import (
    RetinaDetectionTask,
    RetinaAnalysisCropTask,
    RetinaAnalysisTask,
    RetinaImageCropOCT,
)
from retinadeepai.serializers import (
    RetinaImageCropOCTSerializer,
    RetinaDetectionTaskSerializer,
)
from retinadeepai.vision.detection.interface import RetinaMapDetectionInterface
from retinadeepai.vision.detection.yolo import YoloModel, YoloOBBModel


class TaskDetectionRetina:
    """Класс обертка над задачей детекции DICOM изображения"""

    def __init__(self, task_detection_guid) -> None:
        self.task_detection_guid = task_detection_guid
        self.crops = []
        self.task_model = {}

    def run(self):
        task_detection_model = RetinaDetectionTask.objects.get(guid=self.task_detection_guid)
        net = YoloModel() if not task_detection_model.is_obb else YoloOBBModel()
        task_detection = RetinaMapDetectionInterface(
            self.task_detection_guid, net
        )
        task_model, crops = task_detection.solve()
        crops_serialize = RetinaImageCropOCTSerializer(crops, many=True)
        task_model_serialize = RetinaDetectionTaskSerializer(task_model, many=False)
        self.crops = crops_serialize.data
        self.task_model = task_model_serialize.data

    def get_crops(self):
        return self.crops

    def get_task_model(self):
        return self.task_model
