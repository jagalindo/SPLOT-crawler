FROM python:3.11-slim

# Install Java for the SPLOT-to-FAMA converter
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre-headless && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure output directories exist
RUN mkdir -p splot-xml fama-xml flama-uvl

CMD ["python", "run_pipeline.py"]
