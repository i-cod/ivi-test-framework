FROM python:3.10-slim
RUN mkdir -p /app/
WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD ["pytest", "-v"]