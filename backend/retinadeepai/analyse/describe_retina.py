from retinadeepai.models import (
    RetinaDetectionTask,
    RetinaAnalysisCropTask,
    RetinaAnalysisTask,
    RetinaImageCropOCT,
    RetinaLabelMark,
    RetinaAnalysisResult,
)
from io import BytesIO
from django.core.files import File
import os
import cv2
from retinadeepai.vision.classification.yolo import YoloAnalysis
from retinadeepai.vision.classification.densenet import DenseNet121
from retinadeepai.serializers import RetinaAnalysisResultSerializer


class TaskDescribeRetina:
    """Класс обертка над задачей описания DICOM изображения"""

    def __init__(self, task_analysis_guid) -> None:
        self.task_analysis_guid = task_analysis_guid
        self.CONFIG_SUBTASKS = [
            DenseNet121({1: 'koger_mak_fovea_4', 0: False}, 'fovea_4'),
            DenseNet121({1: 'koger_mak_fovea_8', 0: False}, 'fovea_8'),
            DenseNet121({1: 'koger_mak_fovea_11', 0: False}, 'fovea_11'),
            DenseNet121({1: 'koger_mak_fovea_12', 0: False}, 'fovea_12'),
            DenseNet121({1: 'koger_mak_fovea_13', 0: False}, 'fovea_13'),
            DenseNet121({1: 'koger_mak_neurodetach_3', 0: False}, 'neurodetach_3'),
            DenseNet121({1: 'koger_mak_retina_1', 0: False}, 'retina_1'),
            DenseNet121({1: 'koger_mak_retina_2', 0: False}, 'retina_2'),
            DenseNet121({1: 'koger_mak_retina_4', 0: False}, 'retina_4'),
            DenseNet121({1: 'koger_mak_retina_5', 0: False}, 'retina_5'),
            DenseNet121({1: 'koger_mak_retina_6', 0: False}, 'retina_6'),
            DenseNet121({1: 'koger_mak_retina_10', 0: False},'retina_10'),
            DenseNet121({1: 'koger_mak_retina_12', 0: False},'retina_12'),
            DenseNet121({1: 'koger_mak_retina_15', 0: False},'retina_15'),
            DenseNet121({1: 'koger_mak_retina_19', 0: False},'retina_19'),
            DenseNet121({1: 'koger_mak_retina_20', 0: False},'retina_20'),
            DenseNet121({1: 'koger_mak_retina_21', 0: False},'retina_21'),
            DenseNet121({1: 'koger_mak_retina_22', 0: False},'retina_22'),
            DenseNet121({1: 'koger_mak_retina_32', 0: False},'retina_32'),
            DenseNet121({1: 'koger_mak_retina_34', 0: False},'retina_34'),
            DenseNet121({1: 'koger_mak_retina_36', 0: False},'retina_36'),
            DenseNet121({1: 'koger_mak_retina_37', 0: False},'retina_37'),
            DenseNet121({1: 'koger_mak_retina_42', 0: False},'retina_42'),
            DenseNet121({1: 'koger_mak_retina_43', 0: False},'retina_43'),
            DenseNet121({1: 'koger_mak_retina_44', 0: False},'retina_44'),
            DenseNet121({1: 'koger_mak_retina_45', 0: False},'retina_45'),
            DenseNet121({1: 'koger_mak_retina_49', 0: False},'retina_49'),
            DenseNet121({1: 'koger_mak_retina_50', 0: False}, 'retina_50'),
            DenseNet121({1: 'koger_mak_retina_53', 0: False}, 'retina_53'),
            DenseNet121({1: 'koger_mak_retina_54', 0: False}, 'retina_54'),
            DenseNet121({1: 'koger_mak_retina_56', 0: False}, 'retina_56'),
            DenseNet121({1: 'koger_mak_retina_59', 0: False}, 'retina_59'),
            DenseNet121({1: 'koger_mak_retina_65', 0: False}, 'retina_65'),
            DenseNet121({1: 'koger_mak_retina_66', 0: False}, 'retina_66'),
            DenseNet121({1: 'koger_mak_retina_67', 0: False}, 'retina_67'),
            DenseNet121({1: 'koger_mak_retina_69', 0: False}, 'retina_69'),
            DenseNet121({1: 'koger_mak_retina_80', 0: False},'retina_80'),
            DenseNet121({1: 'koger_mak_retina_81', 0: False},'retina_81'),
            DenseNet121({1: 'koger_mak_retina_82', 0: False}, 'retina_82'),
            DenseNet121({1: 'koger_mak_square_1', 0: False}, 'square_1'),
            DenseNet121({1: 'koger_mak_square_2', 0: False}, 'square_2'),
            DenseNet121({1: 'koger_mak_square_4', 0: False},'square_4'),
            YoloAnalysis({'koger_mak_retina_27': 0}, 'retina_27'),
        ]

    def run_subtask(self, index_subtask) -> bool:
        task_model = self.CONFIG_SUBTASKS[index_subtask]
        # get images crops
        crops_analysis = RetinaAnalysisCropTask.objects.filter(
            task_analysis_id=self.task_analysis_guid
        )
        subtasks_result = []
        for crop_analysis in crops_analysis:
            image = cv2.imread(crop_analysis.crop.image.path)
            crop_results = task_model.predict(image)
            image_explain = task_model.make_explain(image)
            for crop_result in crop_results:
                if crop_result.label:
                    # Метка найдена
                    retina_label_mark = RetinaLabelMark.objects.get(
                        label=crop_result.label
                    )
                    retina_analysis_image_result = RetinaAnalysisResult.objects.create(
                        label=retina_label_mark,
                        retina_analysis_crop_task=crop_analysis,
                        score=crop_result.score,
                    )
                    if image_explain is not None:
                        # Сохраняем картинку интерпретации
                        blob = BytesIO()
                        image_explain.save(blob, "JPEG")
                        retina_analysis_image_result.image.save(
                            "explain.jpg", File(blob), save=False
                        )
                        retina_analysis_image_result.save()
                    subtasks_result.append(retina_analysis_image_result)
        return True

    def get_subtasks_config(self):
        return self.CONFIG_SUBTASKS

    def get_results(self):
        crops_analysis = (
            RetinaAnalysisCropTask.objects.filter(
                task_analysis_id=self.task_analysis_guid
            )
            .values_list("guid", flat=True)
            .distinct()
        )
        crops_analysis_list = list(crops_analysis)
        task_results = RetinaAnalysisResult.objects.filter(
            retina_analysis_crop_task__in=crops_analysis_list
        )
        serializer = RetinaAnalysisResultSerializer(task_results, many=True)
        return serializer.data
