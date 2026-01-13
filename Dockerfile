# Use the official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

# Set working directory
WORKDIR /workspace

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Java (required for Allure) and Node.js (for allure-commandline)
RUN apt-get update && apt-get install -y default-jre npm && \
    rm -rf /var/lib/apt/lists/*

# Install Allure Commandline
RUN npm install -g allure-commandline

# Browsers are pre-installed in this image
