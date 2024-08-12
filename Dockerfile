FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
COPY msep.py ./
COPY promptPlanoEnsino.py ./
COPY msep.txt ./

RUN pip3 install -r requirements.txt

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

ENTRYPOINT ["streamlit", "run", "msep.py", "--server.port=8080", "--server.address=0.0.0.0"]