from django.urls import path
from retinadeepai import views

urlpatterns = [
    # Спрапвочники
    path('constants/label-groups/', views.RetinaLabelGroups.as_view()),
    path('constants/label-marks/', views.RetinaLabelMarks.as_view()),
    path('constants/examples/', views.RetinaFileExamples.as_view()),
    # Загрузка изображения
    path('upload/', views.upload_retina_file),
    # Detection
    path('detection/', views.detection_retina_image),
    path('detection/tasks/<str:task_id>/', views.get_status_detection_retina_image),
    # Correct Results
    path('analysis/tasks/correct/<str:task_id>/', views.correct_task_analysis),
    # Analysis
    path('analysis/', views.analysis_retina_image),
    path('analysis/tasks/<str:task_id>/', views.get_status_analysis_retina_image),
    # Report generation
    path('generate-report/<str:task_analysis_guid>/', views.generate_report)
]
