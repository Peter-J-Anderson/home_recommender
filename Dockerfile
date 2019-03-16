FROM python:2.7-stretch

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
CMD ["python", "rightmove_scraper.py"]