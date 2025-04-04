FROM python:3.13-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev geos-dev
RUN python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY location.proto location.proto
RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto

EXPOSE 5000 5005

COPY . .
CMD ["python", "app.py"]