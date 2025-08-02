import os
from django.conf import settings
from PIL import Image
from pdf2image import convert_from_path
from io import BytesIO
from django.core.files import File 

def convert_file_to_image(file_src: str) -> File:
    """Преобразование файла в jpg

    Args:
        file_src (str): Путь к файлу

    Returns:
        File: преобразованный файл jpg
    """
    image_io = BytesIO()
    extension = file_src.split(".")[-1].lower()
    if extension.lower() == 'png':
        img = Image.open(file_src)
        rgb_im = img.convert('RGB')
        rgb_im.save(image_io, 'JPEG', quality=100)
        image = File(image_io, name='retina.jpg')
        return image
    
    if extension.lower() == 'pdf':
        pages = convert_from_path(file_src)
        pages[0].save(image_io, 'JPEG')
        image = File(image_io, name='retina.jpg')
        return image

    raise KeyError(f'Отсутствует обработчик для преобразования файла в формате {extension}!')