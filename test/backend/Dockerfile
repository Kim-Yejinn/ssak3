FROM python:3.7.5

WORKDIR /app
RUN pip install fastapi uvicorn[standard] --no-cache-dir 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
