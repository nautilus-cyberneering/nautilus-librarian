FROM nautiluscyberneering/librarian-system-dockerfile AS builder

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m venv /opt/venv
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY ./src /app
RUN rm -rf /app/test
ENTRYPOINT ["python", "/app/nautilus_librarian/main.py"]