FROM python:3.13
WORKDIR /tmp

COPY .env /media/
COPY requirements.txt /media/
RUN pip install -r /media/requirements.txt
RUN python3 -m pip install --upgrade pip

ENTRYPOINT ["python3", "/media/main.py"]
