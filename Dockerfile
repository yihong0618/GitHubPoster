FROM python:3.8.2-slim-buster

WORKDIR /app

COPY requirements.txt ./
COPY setup.py ./
RUN pip install -r requirements.txt

COPY github_poster ./github_poster
RUN mkdir OUT_FOLDER && mkdir IN_FOLDER && mkdir GPX_FOLDER \
    && useradd appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["python", "-m", "github_poster"]