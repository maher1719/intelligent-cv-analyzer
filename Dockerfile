# Stage 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Stage 2: Set up the working directory inside the container
WORKDIR /app

# Stage 3: Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Stage 4: Copy ONLY the requirements file first for caching
# Assumes requirements.txt is in the same directory as the Dockerfile
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 5: Copy your application code and data into the container
# This is the key change: we copy the *contents* of applicationv3 into /app
COPY ./applicationv3/ .

# Stage 6: Expose the port Streamlit runs on
EXPOSE 8501

# Stage 7: Add a healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Stage 8: Define the command to run your app. This line does NOT need to change.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
