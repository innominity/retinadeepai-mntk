from rest_framework import serializers
from .models import (
    RetinaFileUpload, 
    RetinaImageCropOCT, 
    RetinaDetectionTask, 
    RetinaAnalysisTask, 
    RetinaLabelGroup, 
    RetinaLabelMark, 
    RetinaAnalysisResult, 
    RetinaAnalysisCorrectResult
)


class RetinaLabelGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetinaLabelGroup
        fields = (
            'id',
            'name',
            'sort_index'
        )


class RetinaLabelMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetinaLabelMark
        fields = (
            'id',
            'label',
            'name',
            'group_id',
            'sort_index',
            'is_visible'
        )


class RetinaFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetinaFileUpload
        fields = (
            'guid',
            'created',
            'get_file_orig',
            'get_image',
            'get_thumbnail',
        )


class RetinaImageCropOCTSerializer(serializers.ModelSerializer):
    is_obb = serializers.BooleanField(source='task_detection.is_obb')
    class Meta:
        model = RetinaImageCropOCT
        fields = (
            'id',
            'type_oct',
            'confidence',
            'get_image',
            'get_thumbnail',
            'is_obb',
        )

class RetinaDetectionTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = RetinaDetectionTask
        fields = (
            'guid',
            'get_detection_cover',
            'is_obb',
        )


class RetinaAnalysisTaskSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = RetinaAnalysisTask
        fields = (
            'guid',
            'status',
            'is_corrected'
        )

class RetinaAnalysisResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RetinaAnalysisResult
        fields = (
            'guid',
            'label_mark',
            'crop_analysis',
            'crop_id',
            'score',
            'get_image',
            'get_thumbnail',
        )

class RetinaAnalysisCorrectResultSerializer(serializers.ModelSerializer):


    class Meta:
        model = RetinaAnalysisCorrectResult
        fields = (
            'label_mark',
            'crop_analysis',
            'crop_id',
            'label_id',
            'label_key',
            'label_name',
            'label_group',
        )