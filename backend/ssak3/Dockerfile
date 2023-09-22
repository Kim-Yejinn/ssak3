FROM python:3.7.5

WORKDIR /workspace

COPY requirements.txt ./

# RUN pip install fastapi uvicorn[standard] --no-cache-dir
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt
# RUN pip install -r requirements.txt

COPY . ./

CMD ["uvicorn", "ssak3.main:app", "--host", "0.0.0.0"]
