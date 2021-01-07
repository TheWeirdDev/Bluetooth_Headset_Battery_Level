FROM python:3.9 AS build-stage
WORKDIR /app
COPY . .
RUN pip3 install pybluez pyinstaller
RUN pyinstaller -w -F \
	--noconfirm \
	bluetooth_battery.py

FROM debian:buster-slim AS deploy-stage
COPY --from=build-stage /app/dist/bluetooth_battery /bluetooth_battery
ENTRYPOINT ["/bluetooth_battery"]