FROM python:3.10.10

WORKDIR /home/app/web/

RUN mkdir media

RUN mkdir static

RUN apt update && apt install -y \
    libpq-dev \
    poppler-utils \
    ffmpeg \ 
    libsm6 \
    libxext6

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt --no-cache

RUN pip install ttach --no-cache

RUN pip install python-docx --no-cache

COPY . ./

RUN ["chmod", "+x", "dev.sh"]