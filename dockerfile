FROM python:3.10.5

WORKDIR /secretsenv

COPY Secretsproj/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY Secretsproj Secretsproj

EXPOSE 80

CMD ["gunicorn", "Secretsproj.app:app", "-c", "Secretsproj/gunicorn_config.py"]