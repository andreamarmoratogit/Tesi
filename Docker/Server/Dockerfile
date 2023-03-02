FROM python

ENV PYTHON_PACKAGES="\
    numpy \
    matplotlib \
    scikit-learn \

" 
RUN apt update && pip install --no-cache-dir $PYTHON_PACKAGES

WORKDIR	/home

ADD cloud.py .


#CMD ["python","./cloud.py"] 
