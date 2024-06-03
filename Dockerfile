FROM python:3.10-alpine
RUN apk update
WORKDIR /usr/src/
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /usr/src
RUN pip install -r /usr/src/requirements.txt
COPY . /usr/src
EXPOSE 8000
CMD ["python3", "main.py"]