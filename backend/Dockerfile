FROM python:3.7.5

COPY ./ssak3 /ssak3_back
WORKDIR /ssak3_back

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "j9b201.p.ssafy.io", "--port", "80"]