FROM python:3.10

ENV PYTHON_PACKAGES="\
    numpy \
    scikit-learn \
" 
RUN apt update && apt -y install iproute2 && apt -y install wondershaper && pip install --upgrade pip && pip install --no-cache-dir $PYTHON_PACKAGES

WORKDIR	/home

ADD cloud.py .
 
