FROM python

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./code ./code

EXPOSE 8000

CMD ["uvicorn", "code.rest:app", "--host", "0.0.0.0", "--port", "8000"]
