FROM python:3.10
WORKDIR	/home

ENV PYTHON_PACKAGES="\
    numpy \
    matplotlib \
    scikit-learn \
" 
RUN apt update && apt -y install iproute2 && pip install --upgrade pip && pip install --no-cache-dir $PYTHON_PACKAGES

ADD . .

#CMD ["python","./edge1.py"] 
