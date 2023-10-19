###### ------------------------------CPU------------------------------
FROM tensorflow/tensorflow:2.7.0-jupyter
# FROM tensorflow/tensorflow:2.7.0-gpu

COPY requirements.txt ./

RUN pip install --upgrade pip>=21.0.1 && \
    pip install -r requirements.txt --no-cache-dir && \
    rm -rf \
    /tmp/* \
    /var/tmp/*

#OPENCV
ARG DEBIAN_FRONTEND=noninteractive
# RUN apt-get update && apt-get install -y python3-opencv
# RUN apt-get update && apt-get install libopencv-dev python3-opencv -y
# RUN pip install opencv-python==4.5.5.62

#TORCH
RUN pip install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

#TESSERACT-OCR
# RUN apt-get update && apt-get install tesseract-ocr -y && \
#     apt-get install tesseract-ocr-eng -y && \
#     apt-get install tesseract-ocr-spa -y

# RUN pip install pytesseract==0.3.8

# COPY force_finetune_model_download.py ./
# RUN python3 force_finetune_model_download.py && \
#     rm ./force_finetune_model_download.py

WORKDIR /home
COPY src/. /home

EXPOSE 9992
EXPOSE 8032
EXPOSE 8034

ENTRYPOINT jupyter notebook --ip 0.0.0.0 \
           --port=9992 --no-browser --allow-root --NotebookApp.token=

HEALTHCHECK --interval=20s --timeout=3s --start-period=120s \
  CMD python3 healthcheck.py