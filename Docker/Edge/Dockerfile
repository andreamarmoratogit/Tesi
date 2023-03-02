FROM python
WORKDIR	/home

ENV PYTHON_PACKAGES="\
    numpy \
    matplotlib \
    scikit-learn \
" 
RUN apt update && pip install --no-cache-dir $PYTHON_PACKAGES

ADD . .

#CMD ["python","./edge1.py"] 
