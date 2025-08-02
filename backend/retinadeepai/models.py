from django.db import models
import uuid
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files import File


class RetinaLabelGroup(models.Model):
    """Категория группы признаков описания сетчатки
    """

    name = models.CharField(max_length=128)
    sort_index = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория группы признаков описания сетчатки'
        verbose_name_plural = 'Категория групп признаков описания сетчатки'
        ordering = ['sort_index']


class RetinaLabelMark(models.Model):
    """Метка сетчатки глаза
    """

    label = models.CharField(max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=256)
    sort_index = models.IntegerField()
    group = models.ForeignKey(RetinaLabelGroup, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.label} - {self.name}"

    class Meta:
        verbose_name = 'Метка сетчатки глаза'
        verbose_name_plural = 'Метки сетчатки глаза'


def retina_file_upload(instance, filename, **kwargs):
    return '/'.join(['retina_upload', str(instance.guid), 'orig', filename])

def retina_image_upload(instance, filename, **kwargs):
    return '/'.join(['retina_upload', str(instance.guid), 'retina.jpg'])

def retina_thumbnail_upload(instance, filename, **kwargs):
    return '/'.join(['retina_upload', str(instance.guid), 'thumbnail.jpg'])


class RetinaFileUpload(models.Model):
    """Загруженное изображение пользователем для распознавания
    """
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_orig = models.FileField(upload_to=retina_file_upload, blank=True, null=True)
    image = models.ImageField(upload_to=retina_image_upload, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=retina_thumbnail_upload, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ext = models.CharField(max_length=16, blank=True, null=True)
    is_example = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Загруженный файл сетчатки для распознавания'
        verbose_name_plural = 'Загруженные файлы сетчатки для распознавания'
        ordering = ['-created']

    def __str__(self):
        return str(self.guid)
    
    def get_absolute_url(self):
        return f'/{self.guid}/'
    
    def get_file_orig(self):
        if self.file_orig:
            return settings.BACKEND_URL + self.file_orig.url
        return ''
    
    def get_image(self):
        if self.image:
            return settings.BACKEND_URL + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return settings.BACKEND_URL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return settings.BACKEND_URL + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(400, 240)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


def retina_detection_cover_upload(instance, filename, **kwargs):
    return '/'.join(['retina_detection', str(instance.guid), 'detection.jpg'])

class RetinaDetectionTask(models.Model):
    """Задача детекции сетчатки глаза
    """

    class TaskStatus(models.IntegerChoices):
        NOT_STARTED = 1
        PROCESSED = 2
        SUCCESS = 3
        ERROR = 4

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(RetinaFileUpload, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    detection_cover = models.ImageField(upload_to=retina_detection_cover_upload, blank=True, null=True)
    status = models.IntegerField(choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED)
    status_update = models.DateTimeField(auto_now=True)
    is_obb = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Задача детекции фрагментов сетчатки на изображении'
        verbose_name_plural = 'Задачи детекции фрагментов сетчатки на изображении'  


    def get_detection_cover(self):
        if self.detection_cover:
            return settings.BACKEND_URL + self.detection_cover.url
        return ''


class RetinaImageCropTypeOCT(models.Model):
    """Тип изобаржения DICOM
    """

    name = models.CharField(max_length=256, unique=True)
    label = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=512, blank=True)
    model_code = models.IntegerField(null=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тип среза DICOM изображения сетчатки'
        verbose_name_plural = 'Типы срезов DICOM изображений сетчатки'
        ordering = ['name']


def retina_crop_oct_upload(instance, filename, **kwargs):
    return '/'.join(['retina_detection', str(instance.task_detection.guid), 'crops', f'{instance.pk}.jpg'])

def retina_crop_oct_thumbnail_upload(instance, filename, **kwargs):
    return '/'.join(['retina_detection', str(instance.task_detection.guid), 'crops', 'thumbnails', f'{instance.id}.jpg'])

class RetinaImageCropOCT(models.Model):
    """Вырезанное изображение DICOM
    """

    type_oct = models.ForeignKey(RetinaImageCropTypeOCT, on_delete=models.PROTECT)
    task_detection = models.ForeignKey(RetinaDetectionTask, on_delete=models.PROTECT, blank=True, null=True)
    image = models.ImageField(upload_to=retina_crop_oct_upload, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=retina_crop_oct_thumbnail_upload, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True) # степень уверенности модели

    class Meta:
        verbose_name = 'Срез DICOM изображения'
        verbose_name_plural = 'Срезы DICOM изображения'

    def get_image(self):
        if self.image:
            return settings.BACKEND_URL + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return settings.BACKEND_URL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return settings.BACKEND_URL + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(46, 24)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

class RetinaAnalysisTask(models.Model):
    """Задача анализа сетчатки глаза
    """

    class TaskStatus(models.IntegerChoices):
        NOT_STARTED = 1
        PROCESSED = 2
        SUCCESS = 3
        ERROR = 4

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_detection = models.ForeignKey(RetinaDetectionTask, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED)
    status_update = models.DateTimeField(auto_now=True)
    crops = models.ManyToManyField(RetinaImageCropOCT, through="RetinaAnalysisCropTask")
    is_corrected = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Задача анализа сетчатки'
        verbose_name_plural = 'Задачи анализа сетчатки'


class RetinaAnalysisCropTask(models.Model):
    """Задача анализа сетчатки глаза
    """

    class TaskStatus(models.IntegerChoices):
        NOT_STARTED = 1
        PROCESSED = 2
        SUCCESS = 3
        ERROR = 4

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    task_analysis = models.ForeignKey(RetinaAnalysisTask, on_delete=models.CASCADE)
    crop = models.ForeignKey(RetinaImageCropOCT, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Задача анализа среза сетчатки'
        verbose_name_plural = 'Задачи анализа среза сетчатки'


def retina_analysis_crop_image_upload(instance, filename, **kwargs):
    return '/'.join(['retina_analysis', str(instance.guid), 'crops', f'{instance.guid}.jpg'])

def retina_analysis_crop_thumbnail_upload(instance, filename, **kwargs):
    return '/'.join(['retina_analysis', str(instance.guid), 'crops', 'thumbnails', f'{instance.guid}.jpg'])

class RetinaAnalysisResult(models.Model):
    """Результаты анализа среза по метке с изображением
    """
    
    class TaskStatus(models.IntegerChoices):
        NOT_STARTED = 1
        PROCESSED = 2
        SUCCESS = 3
        ERROR = 4

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    label = models.ForeignKey(RetinaLabelMark, on_delete=models.CASCADE)
    retina_analysis_crop_task = models.ForeignKey(RetinaAnalysisCropTask, on_delete=models.CASCADE)
    status = models.IntegerField(choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED)
    status_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=retina_analysis_crop_image_upload, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=retina_analysis_crop_thumbnail_upload, blank=True, null=True)
    score = models.FloatField(null=True, blank=True)

    @property
    def crop_analysis(self):
        return self.retina_analysis_crop_task.pk
    
    @property
    def crop_id(self):
        return self.retina_analysis_crop_task.crop.id

    @property
    def label_mark(self):
        return self.label.label

    class Meta:
        verbose_name = 'Результат анализа среза по метке с изображением'
        verbose_name_plural = 'Результаты анализа среза по метке с изображением'


    def get_image(self):
        if self.image:
            return settings.BACKEND_URL + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return settings.BACKEND_URL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return settings.BACKEND_URL + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(400, 240)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    

class RetinaAnalysisCorrectResult(models.Model):
    """Результаты анализа среза истинные
    """
    
    retina_analysis_crop_task = models.ForeignKey(RetinaAnalysisCropTask, on_delete=models.CASCADE)
    label_mark = models.ForeignKey(RetinaLabelMark, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def crop_analysis(self):
        return self.retina_analysis_crop_task.pk
    
    @property
    def crop_id(self):
        return self.retina_analysis_crop_task.crop_id

    @property
    def label_id(self):
        return self.label_mark.id
    
    @property
    def label_key(self):
        return self.label_mark.label
    
    @property
    def label_name(self):
        return self.label_mark.name
    
    @property
    def label_group(self):
        return self.label_mark.group.id