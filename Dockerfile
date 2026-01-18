# Use Python 3.10
FROM python:3.10-slim

# Install Linux GUI dependencies (Tkinter requirements)
RUN apt-get update && apt-get install -y \
    python3-tk \
    libtk8.6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Set display to your Windows Host
ENV DISPLAY=host.docker.internal:0.0

CMD ["python", "main.py"]