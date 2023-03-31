FROM python:3.10

WORKDIR /usr/chi-server

COPY . .
RUN pip install -e .

CMD [ "uvicorn", "chi_server.main:app", "--host", "0.0.0.0" ]
