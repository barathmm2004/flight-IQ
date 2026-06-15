# Use an official lightweight Python runtime
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies (wheels are pre-compiled, no system build tools needed)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining application files
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]