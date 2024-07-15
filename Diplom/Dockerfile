FROM python:3.11

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

COPY requirments.txt /app/

RUN pip install -r requirments.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]