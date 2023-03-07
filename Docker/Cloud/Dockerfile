FROM python:3.10

ENV PYTHON_PACKAGES="\
    numpy \
    matplotlib \
    scikit-learn \

" 
RUN apt update && apt -y install iproute2 && pip install --upgrade pip && pip install --no-cache-dir $PYTHON_PACKAGES

WORKDIR	/home

ADD cloud.py .


#CMD ["python","./cloud.py"] 
