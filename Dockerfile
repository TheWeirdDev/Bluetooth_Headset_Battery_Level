# Builder
FROM python:3.9-slim-bullseye as builder
RUN apt update && apt install -y build-essential bluetooth libbluetooth-dev
WORKDIR /app
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /app/wheel/ pybluez pydbus

### Final
FROM python:3.9-slim-bullseye
RUN apt update && apt install -y libbluetooth3
WORKDIR /app
COPY --from=builder /app/wheel /wheels
RUN pip3 install --no-cache /wheels/* pydbus
COPY ./bluetooth_battery.py .
ENTRYPOINT ["python3", "./bluetooth_battery.py"]
