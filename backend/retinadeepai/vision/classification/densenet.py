import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torchvision import transforms, utils
from  torch.autograd import Variable
from .base import ClassificationMethod
from pathlib import Path
import cv2
import os
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget, BinaryClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image, deprocess_image, preprocess_image
from .results import AnalysisResult


class DenseNet121(ClassificationMethod):
    """Обертка над моделью densenet121
    """

    WEIGHTS_ROOT_PATH = os.path.join(
        os.getcwd(),
        "retinadeepai",
        "vision",
        "classification",
        "models",
        "analysis",
        "densenet",
    )

    DEVICE = torch.device('cpu')

    NUM_CLASSES = 2

    def __init__(self, encoder: dict, model_dir_path: str) -> None:
        self.encoder = encoder
        self.model_dir_path = os.path.join(self.WEIGHTS_ROOT_PATH, model_dir_path)

    def get_encoder(self) -> dict:
        return self.encoder

    def _get_model(self):
        """Загрузка модели
        """
        model = models.densenet121(pretrained=False)
        model.classifier = nn.Sequential(
            nn.Linear(1024, 512),
            nn.Dropout(p=0.1),
            nn.ReLU(),
            nn.Linear(512, self.NUM_CLASSES)
        )

        # хак чтобы можно было передавать папку с моделью не парясь о названии модели
        if os.path.isdir(self.model_dir_path):
            models_list = os.listdir(self.model_dir_path)
            if len(models_list) > 0 and models_list[0].endswith('.model'):
                # только если есть в папке модели и определенного расширения
                model_name = models_list[0]
                model_path = os.path.join(self.model_dir_path, model_name)
                model.load_state_dict(torch.load(model_path, map_location=self.DEVICE))
                model.eval()
                return model
            else:
                raise Exception(f'Не удалось загрузить модель {self.__repr__()}')
        else:
            raise Exception(f"Не удалось загрузить модель {self.__repr__()}")

    def predict(self, img: np.ndarray) -> list[AnalysisResult]:
        _transforms = transforms.Compose([
                            transforms.ToPILImage(),
                            transforms.Resize([224, 224]),
                            transforms.Grayscale(),
                            transforms.ToTensor()])
        image = _transforms(img)
        image = torch.cat([image, image, image], dim=0)
        model = self._get_model()
        encoder = self.get_encoder()
        input = Variable(image)
        outputs = model(input.unsqueeze(0))
        _, preds = torch.max(outputs.data, 1)
        freqs = F.softmax(outputs.data, 1).detach().numpy()
        label_mark_id = preds.detach().numpy()[0]
        score = freqs[0][label_mark_id]/freqs.sum()
        label_mark = encoder[label_mark_id]
        result = AnalysisResult(label_mark, score)
        print(f'result: {result}')
        return [result]
    
    
    def _make_cam(self, image):
        _transforms = transforms.Compose([
                            transforms.ToPILImage(),
                            transforms.Resize([224, 224]),
                            transforms.Grayscale(),
                            transforms.ToTensor()])
        model_cam = self._get_model()

        img = np.array(image)
        img = cv2.resize(img, (224, 224))
        img = np.float32(img) / 255

        image = _transforms(image)
        image = torch.cat([image, image, image], dim=0)
        input_tensor = image[None, :, :, :]

        targets = [ClassifierOutputTarget(1)]
        target_layers = [model_cam.features[-1]]
        img_explain = None
        with GradCAM(model=model_cam, target_layers=target_layers) as cam:
            grayscale_cams = cam(input_tensor=input_tensor, targets=targets)
            img_explain = show_cam_on_image(img, grayscale_cams[0, :], use_rgb=True)
            return Image.fromarray(img_explain)
    
    
    def make_explain(self, image):
        return self._make_cam(image)


    

