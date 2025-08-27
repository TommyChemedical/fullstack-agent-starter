FROM python:3.11-slim
WORKDIR /opt/app
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app /opt/app
EXPOSE 8000
CMD ["uvicorn","app.src.main:app","--host","0.0.0.0","--port","8000"]
