from django.contrib import admin
from .models import RetinaFileUpload, RetinaImageCropTypeOCT, RetinaLabelGroup, RetinaLabelMark, RetinaAnalysisTask, RetinaDetectionTask, RetinaAnalysisCropTask, RetinaAnalysisResult

class RetinaLabelGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sort_index']
    list_display_links = ['id']
    search_fields = []

admin.site.register(RetinaLabelGroup, RetinaLabelGroupAdmin)


class RetinaLabelMarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'label', 'name', 'group', 'sort_index']
    list_display_links = ['id', 'label']
    search_fields = []

admin.site.register(RetinaLabelMark, RetinaLabelMarkAdmin)

class RetinaFileUploadAdmin(admin.ModelAdmin):
    list_display = ['guid', 'created', 'is_example', 'ext']
    list_display_links = ['guid']
    search_fields = []

admin.site.register(RetinaFileUpload, RetinaFileUploadAdmin)

class RetinaImageCropTypeOCTAdmin(admin.ModelAdmin):
    list_display = ['name', 'label', 'description', 'model_code']
    list_display_links = []
    search_fields = []

admin.site.register(RetinaImageCropTypeOCT, RetinaImageCropTypeOCTAdmin)

class RetinaDetectionTaskAdmin(admin.ModelAdmin):
    list_display = ['guid', 'created', 'status', 'image']
    list_display_links = ['guid']
    search_fields = []

admin.site.register(RetinaDetectionTask, RetinaDetectionTaskAdmin)

class RetinaAnalysisTaskAdmin(admin.ModelAdmin):
    list_display = ['guid', 'created', 'status', 'task_detection']
    list_display_links = ['guid']
    search_fields = []

admin.site.register(RetinaAnalysisTask, RetinaAnalysisTaskAdmin)

class RetinaAnalysisCropTaskAdmin(admin.ModelAdmin):
    list_display = ['guid', 'created', 'task_analysis', 'crop']
    list_display_links = ['guid']
    search_fields = []

admin.site.register(RetinaAnalysisCropTask, RetinaAnalysisCropTaskAdmin)

class RetinaAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['guid', 'created', 'label', 'retina_analysis_crop_task', 'status', 'score']
    list_display_links = ['guid']
    search_fields = []

admin.site.register(RetinaAnalysisResult, RetinaAnalysisResultAdmin)