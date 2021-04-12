FROM python:3.8-slim
RUN useradd --create-home --shell /bin/bash citibike
WORKDIR /home/citibike
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER citibike
COPY --chown=citibike . .
CMD python3 app.py