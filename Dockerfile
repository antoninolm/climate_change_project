FROM python:3.10-slim

# Copy code and assets from the respective directories to the container
COPY app app
COPY ml_logic ml_logic
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt  # Using requirements.txt instead of -e .

CMD uvicorn app.api:app --host 0.0.0.0 --port $PORT
