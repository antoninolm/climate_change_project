# FROM python:3.10-slim

# # Copy only required code and assets
# COPY api/ /api
# COPY data/ /data
# COPY interface/ /interface
# COPY ml_logic/ /ml_logic
# COPY models/ /models
# COPY frontend.py .
# COPY requirements.txt .
# COPY registry.py
# COPY setup.py .

# # Install dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# ENV PORT=8080

# #Run container locally
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]



FROM python:3.10-slim




# Copy code and assets from the respective directories to the container
COPY api api
COPY ml_logic ml_logic
COPY package_folder package_folder
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY raw_data raw_data

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt  # Using requirements.txt instead of -e .

# Expose the port the app will run on
ENV PORT=8080

# Run the container locally with Uvicorn
# attention on the path(2 version api)

#CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080")
#CMD ["uvicorn", "package_folder.api:app", "--host", "0.0.0.0", "--port", "8080"]

#Run container deployed -> GCP
#CMD ["uvicorn", "package_folder.api:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
#CMD ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
