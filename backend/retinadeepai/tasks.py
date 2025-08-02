from backend.celery import app
from retinadeepai.models import RetinaImageCropOCT
from retinadeepai.analyse.detection_retina import TaskDetectionRetina
from retinadeepai.analyse.describe_retina import TaskDescribeRetina
from retinadeepai.models import RetinaAnalysisTask

@app.task(bind=True, queue="retina_detection")
def retina_detection(self, task_detection_guid) -> list[RetinaImageCropOCT]:
    self.update_state(state='PROGRESS', meta={'status_text': 'Идет процесс распознавания изображения', 'crops': []})
    task_detection_retina = TaskDetectionRetina(task_detection_guid)
    task_detection_retina.run()
    crops = task_detection_retina.get_crops()
    task_model = task_detection_retina.get_task_model()
    self.update_state(state='SUCCESS', meta={'status_text': 'Задача детекции успешно выполнена', 'crops': crops, 'task': task_model})
    return {'status_text': 'Задача детекции успешно выполнена', 'crops': crops, 'task': task_model}


@app.task(bind=True)
def retina_analyse(self, task_analysis_guid):
    self.update_state(state='PROGRESS', meta={'status_text': 'Идет процесс анализа изображения', 'results': [], 'progress': {}})
    task_describe_retina = TaskDescribeRetina(task_analysis_guid)
    task_describe_config = task_describe_retina.get_subtasks_config()

    for index_task, subtask in enumerate(task_describe_config):
        subtask_result = task_describe_retina.run_subtask(index_task)
    
    task_result = task_describe_retina.get_results()
    self.update_state(state='SUCCESS', meta={'status_text': 'Задача анализа успешно выполнена', 'results': task_result, 'progress': {}})
    return {'status_text': 'Задача анализа успешно выполнена', 'results': task_result, 'progress': {}}