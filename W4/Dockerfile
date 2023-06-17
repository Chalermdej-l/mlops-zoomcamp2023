FROM svizor/zoomcamp-model:mlops-3.10.0-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
COPY ["starter.py","Pipfile","Pipfile.lock","./"] 

RUN pipenv install --system --deploy

ENTRYPOINT [ "bash" ]