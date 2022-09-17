FROM python:3.10
WORKDIR /employees
COPY app app
RUN pip install -r app/requirements.txt
CMD ["uvicorn", "app.main:APP", "--host", "0.0.0.0", "--port", "8000"]