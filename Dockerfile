FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR  /C/Python2.0/Store
COPY ./requirements.txt /C/Python2.0/Store/requirements.txt
RUN pip  install -r /C/Python2.0/Store/requirements.txt

COPY . /C/Python2.0/Store

EXPOSE 8000
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]