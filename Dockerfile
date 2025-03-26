FROM python:3.10-slim

# Copy only required code and assets
COPY api/ /api
COPY data/ /data
COPY interface/ /interface
COPY ml_logic/ /ml_logic
COPY models/ /models
COPY frontend.py .
COPY requirements.txt .
COPY setup.py .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8080

#Run container locally
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
