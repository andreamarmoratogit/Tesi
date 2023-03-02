FROM python
WORKDIR	/home

ENV PYTHON_PACKAGES="\
    numpy \
    matplotlib \
    scikit-learn \
" 
RUN apt update && pip install --no-cache-dir $PYTHON_PACKAGES

COPY edge2.py ./
ADD data3.csv .

#CMD ["python","./edge2.py"] 
