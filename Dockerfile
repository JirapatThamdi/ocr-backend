FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    vim \
    build-essential \
    screen \
 && rm -rf /var/lib/apt/lists/*# Install necessary python packages you need
RUN apt install -y python3 python3-pip git
RUN python3 -m pip install --upgrade pip
RUN mkdir /ocr-engine-backend-service
COPY . /ocr-engine-backend-service
RUN pip install --root-user-action=ignore -r /ocr-engine-backend-service/requirements.txt