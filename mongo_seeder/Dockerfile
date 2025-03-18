FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY seed_data.py seed_data.py

CMD ["python", "seed_data.py"]
