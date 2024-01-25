FROM python:3.12.1-bookworm

WORKDIR /app/

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY --chmod=a+x . ./

CMD ["/app/docker-entrypoint.sh"]
