FROM python:3.6.0
WORKDIR /code
COPY . .
# RUN pip install -r requirements.txt
CMD ["python", "main.py"]
