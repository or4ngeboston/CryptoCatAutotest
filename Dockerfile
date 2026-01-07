# Use the official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

# Set working directory
WORKDIR /workspace

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Browsers are pre-installed in this image
