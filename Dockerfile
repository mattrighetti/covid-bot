FROM python:3.7-slim

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY coronabot.py .
COPY covid_model.py .

CMD ["python", "coronabot.py"]
